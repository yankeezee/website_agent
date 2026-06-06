from __future__ import annotations

from dataclasses import dataclass

from website_agent.agent import Agent
from website_agent.schemas.quality_verdict import QualityVerdict
from website_agent.schemas.site_blueprint import SiteBlueprint


@dataclass
class JudgeAgent(Agent[SiteBlueprint, QualityVerdict]):
    def run(self, input_data: SiteBlueprint) -> QualityVerdict:
        raise NotImplementedError("Judging is not implemented yet.")
