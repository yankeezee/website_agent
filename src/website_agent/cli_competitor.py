from __future__ import annotations

from website_agent.env import load_environment

load_environment()

from website_agent.agents.competitor_research import CompetitorResearchAgent


def main() -> None:
    agent = CompetitorResearchAgent()
    output = agent.run()
    print(output.model_dump_json(indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
