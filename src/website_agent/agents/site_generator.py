from __future__ import annotations

from dataclasses import dataclass

from website_agent.agent import Agent
from website_agent.schemas.business_profile import BusinessProfile
from website_agent.schemas.site_blueprint import SiteBlueprint
from website_agent.schemas.ux_insights import UXInsights


@dataclass
class SiteGeneratorAgent(Agent[tuple[BusinessProfile, UXInsights], SiteBlueprint]):
    def run(self, input_data: tuple[BusinessProfile, UXInsights]) -> SiteBlueprint:
        raise NotImplementedError("Site generation is not implemented yet.")
