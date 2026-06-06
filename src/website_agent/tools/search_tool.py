from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from website_agent.env import load_environment


TAVILY_SEARCH_URL = "https://api.tavily.com/search"


@dataclass(frozen=True)
class SearchResult:
    title: str
    url: str
    content: str | None = None
    score: float | None = None
    raw_content: str | None = None
    favicon: str | None = None


class SearchTool:
    def __init__(self, api_key: str | None = None) -> None:
        load_environment()
        self.api_key = api_key or os.getenv("TAVILY_API_KEY")

    def run(
        self,
        query: str,
        *,
        max_results: int = 5,
        search_depth: str = "basic",
        country: str | None = None,
        include_domains: list[str] | None = None,
        exclude_domains: list[str] | None = None,
        include_raw_content: bool = False,
    ) -> list[SearchResult]:
        if not self.api_key:
            raise RuntimeError("Set TAVILY_API_KEY before using SearchTool.")

        payload: dict[str, Any] = {
            "query": query,
            "max_results": max_results,
            "search_depth": search_depth,
            "include_answer": False,
            "include_raw_content": include_raw_content,
            "topic": "general",
        }
        if country:
            payload["country"] = country
        if include_domains:
            payload["include_domains"] = include_domains
        if exclude_domains:
            payload["exclude_domains"] = exclude_domains

        request = Request(
            TAVILY_SEARCH_URL,
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
            raise RuntimeError(f"Tavily search failed: {error.code} {error.reason}") from error
        except URLError as error:
            raise RuntimeError(f"Tavily search failed: {error.reason}") from error

        results: list[SearchResult] = []
        for item in response_payload.get("results", []):
            results.append(
                SearchResult(
                    title=item.get("title", ""),
                    url=item.get("url", ""),
                    content=item.get("content"),
                    score=item.get("score"),
                    raw_content=item.get("raw_content"),
                    favicon=item.get("favicon"),
                )
            )
        return results
