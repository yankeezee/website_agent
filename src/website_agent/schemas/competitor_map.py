from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field, HttpUrl


Region = Literal["russia", "europe", "asia", "america"]


class CompetitorEntry(BaseModel):
    url: HttpUrl = Field(..., description="Competitor website URL")
    region: Region = Field(..., description="Market region for this competitor")
    strengths: list[str] = Field(..., description="Observed strengths from the site")
    structure: list[str] = Field(..., description="Observed site structure and sections")


class CompetitorMap(BaseModel):
    competitors: list[CompetitorEntry] = Field(
        default_factory=list,
        description="List of extracted competitor sites",
    )
