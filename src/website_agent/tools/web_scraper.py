from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from website_agent.env import load_environment


TAVILY_EXTRACT_URL = "https://api.tavily.com/extract"


@dataclass(frozen=True)
class ScrapedPage:
    url: str
    region: str
    content: str
    favicon: str | None = None


class WebScraperTool:
    def __init__(self, api_key: str | None = None) -> None:
        load_environment()
        self.api_key = api_key or os.getenv("TAVILY_API_KEY")

    def run(
        self,
        urls: list[str],
        *,
        region: str,
        query: str | None = None,
    ) -> list[ScrapedPage]:
        if not self.api_key:
            raise RuntimeError("Set TAVILY_API_KEY before using WebScraperTool.")
        if not urls:
            return []

        payload: dict[str, Any] = {
            "urls": urls,
            "extract_depth": "basic",
            "format": "text",
            "include_favicon": True,
        }
        if query:
            payload["query"] = query

        request = Request(
            TAVILY_EXTRACT_URL,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )

        try:
            with urlopen(request, timeout=60) as response:
                response_payload = json.loads(response.read().decode("utf-8"))
        except HTTPError as error:
            raise RuntimeError(f"Tavily extract failed: {error.code} {error.reason}") from error
        except URLError as error:
            raise RuntimeError(f"Tavily extract failed: {error.reason}") from error

        pages: list[ScrapedPage] = []
        for item in response_payload.get("results", []):
            pages.append(
                ScrapedPage(
                    url=item.get("url", ""),
                    region=region,
                    content=item.get("raw_content") or "",
                    favicon=item.get("favicon"),
                )
            )
        return pages
