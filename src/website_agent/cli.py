from __future__ import annotations

from pathlib import Path

from website_agent.env import load_environment

load_environment()

from website_agent.agents.business_analyst import BusinessAnalystAgent
from website_agent.orchestrator import Orchestrator
from website_agent.tools.context_loader import DEFAULT_CONTEXT_DIR
from website_agent.tools.output_store import save_business_profile


def main() -> None:
    context_dir = Path(DEFAULT_CONTEXT_DIR)
    orchestrator = Orchestrator(business_analyst=BusinessAnalystAgent())
    profile = orchestrator.run(context_dir)
    output_path = save_business_profile(profile)
    print(output_path.as_posix())


if __name__ == "__main__":
    main()
