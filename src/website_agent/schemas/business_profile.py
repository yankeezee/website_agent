from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class BusinessProfile(BaseModel):
    company_name: str = Field(..., description="Name of the company")
    product: str = Field(..., description="What the business sells or offers")
    audience: str = Field(..., description="Who the business is for")
    pain_points: list[str] = Field(..., description="Key customer pain points")
    value_proposition: str = Field(..., description="Why customers should choose it")
    key_features: list[str] = Field(..., description="Main features or capabilities")
    tone: Literal["formal", "friendly", "premium", "bold", "technical"] = Field(
        ..., description="Overall brand tone"
    )
    industry: str = Field(..., description="Business industry or market segment")
    competitors: list[str] = Field(..., description="Known or implied competitors")
