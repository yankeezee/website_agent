from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from website_agent.agents.competitor_research import CompetitorResearchAgent
from website_agent.agents.business_analyst import BusinessAnalystAgent
from website_agent.schemas.business_profile import BusinessProfile
from website_agent.schemas.competitor_map import CompetitorMap
from website_agent.tools.context_loader import DEFAULT_CONTEXT_DIR


@dataclass
class Orchestrator:
    business_analyst: BusinessAnalystAgent
    competitor_research: CompetitorResearchAgent | None = None

    def run(self, context_dir: Path | str) -> BusinessProfile:
        return self.business_analyst.run(context_dir)

    def run_competitor_research(
        self,
        input_data: BusinessProfile | None = None,
        context_dir: Path | str | None = None,
    ) -> CompetitorMap:
        agent = self.competitor_research or CompetitorResearchAgent(
            business_analyst=self.business_analyst
        )
        return agent.run(input_data=input_data, context_dir=context_dir or DEFAULT_CONTEXT_DIR)
