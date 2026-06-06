# Architecture

## Scope

Single-business workspace. All analysis is driven by files inside `src/website_agent/context/`.

## Pipeline

```text
Context files
    ↓
Business Analyst Agent
    ↓
Structured business profile
    ↓
Competitor Research Agent
    ↓
UX Synthesis Agent
    ↓
Site Generator Agent
    ↓
Judge Agent
    ↓
Improved site package
```

## Layers

- `Input Layer` - reads business context files.
- `Analysis Layer` - extracts the structured business profile.
- `Research Layer` - gathers competitor data.
- `Synthesis Layer` - turns research into UX direction.
- `Generation Layer` - produces site structure, copy, and design prompt.
- `Evaluation Layer` - checks quality and completeness.
- `Output Layer` - stores final artifacts.

## Agents

- `Business Analyst Agent`
- `Competitor Research Agent`
- `UX Synthesis Agent`
- `Site Generator Agent`
- `Judge Agent`

## Tools

- `Search`
- `Web Scraper`
- `LLM`
- `Context Loader`

## Shared Schemas

- `BusinessProfile`
- `CompetitorMap`
- `MarketSummary`
- `UXInsights`
- `SiteBlueprint`
- `QualityVerdict`

## Current Output

- `output/business-profile.json`
- `output/competitor-map.json`

## Python Structure

```text
website_agent/
├── pyproject.toml
├── ARCHITECTURE.md
└── src/
    └── website_agent/
        ├── __init__.py
        ├── agent.py
        ├── orchestrator.py
        ├── context/
        │   └── RKM.txt
        ├── agents/
        │   ├── __init__.py
        │   └── business_analyst.py
        ├── prompts/
        │   ├── __init__.py
        │   └── business_analyst.py
        ├── schemas/
        │   ├── __init__.py
        │   ├── business_profile.py
        │   ├── competitor_map.py
        │   ├── market_summary.py
        │   ├── quality_verdict.py
        │   ├── site_blueprint.py
        │   └── ux_insights.py
        └── tools/
            ├── __init__.py
            ├── context_loader.py
            ├── llm.py
            ├── search_tool.py
            └── web_scraper.py
```

## Boundary

This step only adds the shared architecture skeleton. Agent logic can be filled in next without changing the contract between modules.
