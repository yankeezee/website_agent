from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from website_agent.agents.business_analyst import BusinessAnalystAgent
from website_agent.schemas.business_profile import BusinessProfile


@dataclass
class Orchestrator:
    business_analyst: BusinessAnalystAgent

    def run(self, context_dir: Path | str) -> BusinessProfile:
        return self.business_analyst.run(context_dir)
