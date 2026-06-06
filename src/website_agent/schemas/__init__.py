"""Shared data schemas."""

from website_agent.schemas.business_profile import BusinessProfile
from website_agent.schemas.competitor_map import CompetitorMap
from website_agent.schemas.market_summary import MarketSummary
from website_agent.schemas.quality_verdict import QualityVerdict
from website_agent.schemas.site_blueprint import SiteBlueprint
from website_agent.schemas.ux_insights import UXInsights

__all__ = [
    "BusinessProfile",
    "CompetitorMap",
    "MarketSummary",
    "QualityVerdict",
    "SiteBlueprint",
    "UXInsights",
]
