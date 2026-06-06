from __future__ import annotations

import json
from dataclasses import dataclass
from os import getenv
from pathlib import Path

from google import genai

from website_agent.schemas.business_profile import BusinessProfile
from website_agent.prompts.business_analyst import (
    BUSINESS_ANALYST_SYSTEM_PROMPT,
    BUSINESS_ANALYST_USER_PROMPT,
)
from website_agent.tools.context_loader import (
    DEFAULT_CONTEXT_DIR,
    BusinessContextBundle,
    load_business_context_bundle,
)


@dataclass
class BusinessAnalystAgent:
    """Extracts a structured business profile from company context files."""

    client: genai.Client | None = None
    model: str = "gemini-2.5-flash"
    system_prompt: str = BUSINESS_ANALYST_SYSTEM_PROMPT

    def _get_client(self) -> genai.Client:
        if self.client is None:
            api_key = getenv("GEMINI_API_KEY") or getenv("GOOGLE_API_KEY")
            if not api_key:
                raise RuntimeError(
                    "Set GEMINI_API_KEY (or GOOGLE_API_KEY) before running the agent."
                )
            self.client = genai.Client(api_key=api_key)
        return self.client

    def build_user_prompt(self, context_bundle: BusinessContextBundle) -> str:
        return BUSINESS_ANALYST_USER_PROMPT.format(
            context_text=context_bundle.to_prompt_text(),
        )

    def parse(self, data: dict) -> BusinessProfile:
        return BusinessProfile.model_validate(data)

    def analyze_context(
        self,
        context_dir: Path | str = DEFAULT_CONTEXT_DIR,
    ) -> BusinessProfile:
        context_bundle = load_business_context_bundle(context_dir)
        user_prompt = self.build_user_prompt(context_bundle)

        response = self._get_client().models.generate_content(
            model=self.model,
            contents=user_prompt,
            config=genai.types.GenerateContentConfig(
                system_instruction=self.system_prompt,
                response_mime_type="application/json",
                response_json_schema=BusinessProfile.model_json_schema(),
                temperature=0,
            ),
        )

        if not response.text:
            raise RuntimeError("Model returned an empty response.")

        return self.parse(json.loads(response.text))

    def run(self, context_dir: Path | str = DEFAULT_CONTEXT_DIR) -> BusinessProfile:
        return self.analyze_context(context_dir)
