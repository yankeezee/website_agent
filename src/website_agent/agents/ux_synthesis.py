from __future__ import annotations

from dataclasses import dataclass

from website_agent.agent import Agent
from website_agent.schemas.business_profile import BusinessProfile
from website_agent.schemas.competitor_map import CompetitorMap
from website_agent.schemas.ux_insights import UXInsights


@dataclass
class UXSynthesisAgent(Agent[tuple[BusinessProfile, CompetitorMap], UXInsights]):
    def run(self, input_data: tuple[BusinessProfile, CompetitorMap]) -> UXInsights:
        raise NotImplementedError("UX synthesis is not implemented yet.")
