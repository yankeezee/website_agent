from __future__ import annotations

import json
from pathlib import Path

from website_agent.schemas.business_profile import BusinessProfile


DEFAULT_OUTPUT_PATH = Path("output") / "business-profile.json"


def save_business_profile(
    profile: BusinessProfile,
    output_path: Path | str = DEFAULT_OUTPUT_PATH,
) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(profile.model_dump(), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return path
