from __future__ import annotations

REGION_SEARCH_TEMPLATES = {
    "russia": (
        "{company_name} {industry} competitors Russia site"
    ),
    "europe": (
        "{company_name} {industry} competitors Europe site"
    ),
    "asia": (
        "{company_name} {industry} competitors Asia site"
    ),
    "america": (
        "{company_name} {industry} competitors US site"
    ),
}

REGION_TAVILY_COUNTRY = {
    "russia": "russia",
    "europe": "germany",
    "asia": "singapore",
    "america": "united states",
}

COMPETITOR_SYNTHESIS_SYSTEM_PROMPT = """You are a senior market research analyst.

You receive a business profile, search results, and extracted competitor page text.
Return only JSON that matches the schema.
Exclude irrelevant or non-competing websites.
For each competitor, derive concise strengths and a concise site structure.
Do not add commentary, markdown, or extra fields.
"""

COMPETITOR_SYNTHESIS_USER_PROMPT = """Business profile:
{business_profile_json}

Region:
{region}

Search results:
{search_results_json}

Scraped pages:
{scraped_pages_json}
"""
