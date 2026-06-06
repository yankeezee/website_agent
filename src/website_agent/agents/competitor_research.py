from __future__ import annotations

from dataclasses import dataclass

from website_agent.agent import Agent
from website_agent.schemas.competitor_map import CompetitorMap
from website_agent.schemas.business_profile import BusinessProfile


@dataclass
class CompetitorResearchAgent(Agent[BusinessProfile, CompetitorMap]):
    def run(self, input_data: BusinessProfile) -> CompetitorMap:
        raise NotImplementedError("Competitor research is not implemented yet.")
