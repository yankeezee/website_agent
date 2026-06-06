from __future__ import annotations

import json
from pathlib import Path

from website_agent.schemas.business_profile import BusinessProfile
from website_agent.schemas.competitor_map import CompetitorMap


DEFAULT_OUTPUT_PATH = Path("output") / "business-profile.json"
DEFAULT_COMPETITOR_MAP_PATH = Path("output") / "competitor-map.json"


def _save_json(data: object, output_path: Path | str) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if hasattr(data, "model_dump"):
        data = data.model_dump(mode="json")
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return path


def save_business_profile(
    profile: BusinessProfile,
    output_path: Path | str = DEFAULT_OUTPUT_PATH,
) -> Path:
    return _save_json(profile, output_path)


def load_business_profile(
    output_path: Path | str = DEFAULT_OUTPUT_PATH,
) -> BusinessProfile:
    path = Path(output_path)
    if not path.exists():
        raise FileNotFoundError(f"Business profile not found: {path}")
    return BusinessProfile.model_validate_json(path.read_text(encoding="utf-8"))


def save_competitor_map(
    competitor_map: CompetitorMap,
    output_path: Path | str = DEFAULT_COMPETITOR_MAP_PATH,
) -> Path:
    return _save_json(competitor_map, output_path)
