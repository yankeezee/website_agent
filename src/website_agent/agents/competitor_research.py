from __future__ import annotations

import json
import time
from dataclasses import dataclass
from os import getenv
from pathlib import Path

from google import genai
from google.genai.errors import ServerError

from website_agent.agent import Agent
from website_agent.env import load_environment
from website_agent.schemas.business_profile import BusinessProfile
from website_agent.schemas.competitor_map import CompetitorMap, Region
from website_agent.agents.business_analyst import BusinessAnalystAgent
from website_agent.prompts.competitor_research import (
    COMPETITOR_SYNTHESIS_SYSTEM_PROMPT,
    COMPETITOR_SYNTHESIS_USER_PROMPT,
    REGION_SEARCH_TEMPLATES,
    REGION_TAVILY_COUNTRY,
)
from website_agent.tools.context_loader import DEFAULT_CONTEXT_DIR
from website_agent.tools.output_store import (
    DEFAULT_COMPETITOR_MAP_PATH,
    DEFAULT_OUTPUT_PATH,
    load_business_profile,
    save_business_profile,
    save_competitor_map,
)
from website_agent.tools.search_tool import SearchResult, SearchTool
from website_agent.tools.web_scraper import ScrapedPage, WebScraperTool


@dataclass
class CompetitorResearchAgent(Agent[BusinessProfile, CompetitorMap]):
    client: genai.Client | None = None
    model: str = "gemini-2.5-flash"
    search_tool: SearchTool | None = None
    web_scraper: WebScraperTool | None = None
    business_analyst: BusinessAnalystAgent | None = None

    def _get_client(self) -> genai.Client:
        load_environment()
        if self.client is None:
            api_key = getenv("GEMINI_API_KEY") or getenv("GOOGLE_API_KEY")
            if not api_key:
                raise RuntimeError(
                    "Set GEMINI_API_KEY (or GOOGLE_API_KEY) before running the agent."
                )
            self.client = genai.Client(api_key=api_key)
        return self.client

    def _get_model_name(self) -> str:
        return getenv("COMPETITOR_RESEARCH_MODEL") or self.model

    def _get_search_tool(self) -> SearchTool:
        if self.search_tool is None:
            self.search_tool = SearchTool()
        return self.search_tool

    def _get_web_scraper(self) -> WebScraperTool:
        if self.web_scraper is None:
            self.web_scraper = WebScraperTool()
        return self.web_scraper

    def _resolve_business_profile(
        self,
        input_data: BusinessProfile | None,
        context_dir: Path | str = DEFAULT_CONTEXT_DIR,
    ) -> BusinessProfile:
        if isinstance(input_data, BusinessProfile):
            return input_data

        try:
            return load_business_profile(DEFAULT_OUTPUT_PATH)
        except FileNotFoundError:
            analyst = self.business_analyst or BusinessAnalystAgent()
            profile = analyst.run(context_dir)
            save_business_profile(profile, DEFAULT_OUTPUT_PATH)
            return profile

    def _build_search_query(self, business_profile: BusinessProfile, region: Region) -> str:
        template = REGION_SEARCH_TEMPLATES[region]
        return template.format(
            company_name=business_profile.company_name,
            product=business_profile.product,
            audience=business_profile.audience,
            value_proposition=business_profile.value_proposition,
            industry=business_profile.industry,
        )

    def _search_region(
        self,
        business_profile: BusinessProfile,
        region: Region,
    ) -> list[SearchResult]:
        query = self._build_search_query(business_profile, region)
        country = REGION_TAVILY_COUNTRY[region]
        return self._get_search_tool().run(
            query,
            max_results=5,
            search_depth="basic",
            country=country,
            include_raw_content=False,
        )

    def _collect_search_results(
        self,
        business_profile: BusinessProfile,
    ) -> dict[Region, list[SearchResult]]:
        region_results: dict[Region, list[SearchResult]] = {}
        for region in ("russia", "europe", "asia", "america"):
            results = self._search_region(business_profile, region)
            unique_results: list[SearchResult] = []
            seen_urls: set[str] = set()
            for result in results:
                if not result.url or result.url in seen_urls:
                    continue
                seen_urls.add(result.url)
                unique_results.append(result)
            region_results[region] = unique_results
        return region_results

    def _scrape_region_results(
        self,
        region_results: dict[Region, list[SearchResult]],
    ) -> dict[Region, list[ScrapedPage]]:
        scraped_pages: dict[Region, list[ScrapedPage]] = {}
        for region, results in region_results.items():
            urls = [result.url for result in results]
            query = " ".join(result.title for result in results if result.title).strip() or None
            pages = self._get_web_scraper().run(urls, region=region, query=query)
            scraped_pages[region] = pages
        return scraped_pages

    def _truncate(self, value: str, limit: int = 2500) -> str:
        cleaned = value.strip()
        if len(cleaned) <= limit:
            return cleaned
        return cleaned[: limit - 3] + "..."

    def _synthesize(
        self,
        business_profile: BusinessProfile,
        region_results: dict[Region, list[SearchResult]],
        scraped_pages: dict[Region, list[ScrapedPage]],
    ) -> CompetitorMap:
        payload = {}
        for region in ("russia", "europe", "asia", "america"):
            results = region_results[region]
            pages = scraped_pages[region]
            payload[region] = {
                "search_results": [
                    {
                        "title": result.title,
                        "url": result.url,
                        "content": self._truncate(result.content or "", 800),
                    }
                    for result in results
                ],
                "scraped_pages": [
                    {
                        "url": page.url,
                        "content": self._truncate(page.content, 2500),
                        "favicon": page.favicon,
                    }
                    for page in pages
                ],
            }

        last_error: Exception | None = None
        response = None
        for attempt in range(3):
            try:
                response = self._get_client().models.generate_content(
                    model=self._get_model_name(),
                    contents=COMPETITOR_SYNTHESIS_USER_PROMPT.format(
                        business_profile_json=json.dumps(
                            business_profile.model_dump(), ensure_ascii=False, indent=2
                        ),
                        region="all",
                        search_results_json=json.dumps(
                            {region: data["search_results"] for region, data in payload.items()},
                            ensure_ascii=False,
                            indent=2,
                        ),
                        scraped_pages_json=json.dumps(
                            {region: data["scraped_pages"] for region, data in payload.items()},
                            ensure_ascii=False,
                            indent=2,
                        ),
                    ),
                    config=genai.types.GenerateContentConfig(
                        system_instruction=COMPETITOR_SYNTHESIS_SYSTEM_PROMPT,
                        response_mime_type="application/json",
                        response_json_schema=CompetitorMap.model_json_schema(),
                        temperature=0,
                    ),
                )
                last_error = None
                break
            except ServerError as error:
                last_error = error
                if getattr(error, "code", None) != 503 or attempt == 2:
                    raise
                time.sleep(2 ** attempt)

        if last_error is not None:
            raise last_error

        if not response.text:
            raise RuntimeError("Model returned an empty competitor research response.")

        data = json.loads(response.text)
        competitor_map = CompetitorMap.model_validate(data)
        return competitor_map

    def run(
        self,
        input_data: BusinessProfile | None = None,
        context_dir: Path | str = DEFAULT_CONTEXT_DIR,
        output_path: Path | str = DEFAULT_COMPETITOR_MAP_PATH,
    ) -> CompetitorMap:
        business_profile = self._resolve_business_profile(input_data, context_dir)
        region_results = self._collect_search_results(business_profile)
        scraped_pages = self._scrape_region_results(region_results)
        competitor_map = self._synthesize(business_profile, region_results, scraped_pages)
        save_competitor_map(competitor_map, output_path)
        return competitor_map
