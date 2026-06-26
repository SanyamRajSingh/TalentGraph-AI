import re
from collections.abc import Iterable
from typing import Any

from app.domain.candidate_twin import CandidateTimelineEntry, GrowthStage

SCORE_FIELDS = (
    "technical_depth",
    "learning_velocity",
    "leadership",
    "ownership",
    "communication",
    "project_complexity",
    "collaboration",
    "consistency",
    "confidence",
)


def clamp_score(value: Any, default: int = 50) -> int:
    try:
        score = int(round(float(value)))
    except (TypeError, ValueError):
        score = default
    return max(0, min(100, score))


def normalize_list(values: Any) -> list[str]:
    if isinstance(values, str):
        values = [part.strip() for part in values.split(",")]
    if not isinstance(values, Iterable):
        return []

    seen: set[str] = set()
    normalized: list[str] = []
    for value in values:
        if not isinstance(value, str):
            continue
        item = value.strip()
        key = item.casefold()
        if item and key not in seen:
            seen.add(key)
            normalized.append(item)
    return normalized


def build_timeline(raw_text: str, structured_fields: dict[str, object]) -> list[CandidateTimelineEntry]:
    years = structured_fields.get("years")
    if not isinstance(years, list):
        years = []
    normalized_years = sorted({int(year) for year in years if isinstance(year, int | str) and str(year).isdigit()})

    if not normalized_years:
        normalized_years = sorted({int(year) for year in re.findall(r"\b(20[0-3][0-9])\b", raw_text)})

    events: list[CandidateTimelineEntry] = []
    skills = normalize_list(structured_fields.get("skills"))
    projects = normalize_list(structured_fields.get("projects"))
    experiences = normalize_list(structured_fields.get("experiences"))

    for index, year in enumerate(normalized_years):
        if index == 0 and skills:
            event = f"Built foundation in {skills[0]}"
        elif index - 1 < len(projects):
            event = projects[index - 1]
        elif index - 1 < len(experiences):
            event = experiences[index - 1]
        else:
            event = "Expanded professional experience"
        events.append(CandidateTimelineEntry(year=year, event=event[:140]))

    return events


def infer_growth_stage(metrics: dict[str, int], skills: list[str], projects: list[str], domains: list[str]) -> GrowthStage:
    technical = metrics["technical_depth"]
    leadership = metrics["leadership"]
    ownership = metrics["ownership"]
    complexity = metrics["project_complexity"]

    if leadership >= 70 and ownership >= 70:
        return GrowthStage.EMERGING_LEADER
    if "Machine Learning" in skills and any(domain in domains for domain in ("Machine Learning", "FinTech")):
        return GrowthStage.RESEARCHER if complexity >= 75 else GrowthStage.HYBRID
    if technical >= 80 and complexity >= 75:
        return GrowthStage.TECHNICAL_SPECIALIST
    if ownership >= 75 or len(projects) >= 2:
        return GrowthStage.BUILDER
    if metrics["communication"] >= 75 and metrics["collaboration"] >= 70:
        return GrowthStage.OPERATOR
    return GrowthStage.EXPLORER
