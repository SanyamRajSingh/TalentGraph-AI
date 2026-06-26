from collections.abc import Iterable
from typing import Any

from app.domain.role_dna import RoleDNAProfile, WorkEnvironmentAttributes

SCORE_FIELDS = (
    "technical_depth",
    "problem_solving",
    "communication",
    "ownership",
    "leadership",
    "learning_agility",
    "ambiguity_tolerance",
    "collaboration",
    "startup_vs_enterprise_environment",
    "confidence",
)

WEIGHT_FIELDS = (
    "technical_depth",
    "problem_solving",
    "communication",
    "ownership",
    "leadership",
    "learning_agility",
    "ambiguity_tolerance",
    "collaboration",
)

FINGERPRINTS = {
    "builder": "Builder",
    "researcher": "Researcher",
    "operator": "Operator",
    "builder_researcher": "Builder-Researcher Hybrid",
    "high_ambiguity_specialist": "High-Ambiguity Technical Specialist",
}


def clamp_score(value: Any, default: int = 50) -> int:
    try:
        score = int(round(float(value)))
    except (TypeError, ValueError):
        score = default
    return max(0, min(100, score))


def normalize_text(value: Any, default: str) -> str:
    if isinstance(value, str) and value.strip():
        return value.strip()
    return default


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


def normalize_weights(raw_weights: Any, fallback_keys: list[str]) -> dict[str, int]:
    if not isinstance(raw_weights, dict):
        raw_weights = {}

    weights: dict[str, int] = {}
    keys = list(dict.fromkeys([*fallback_keys, *[str(key) for key in raw_weights.keys()]]))
    for key in keys:
        weights[key] = max(1, clamp_score(raw_weights.get(key), default=10))

    total = sum(weights.values())
    if total <= 0:
        return {}

    scaled = {key: int(round(value * 100 / total)) for key, value in weights.items()}
    drift = 100 - sum(scaled.values())
    if scaled and drift:
        top_key = max(scaled, key=scaled.get)
        scaled[top_key] = max(0, scaled[top_key] + drift)
    return scaled


def infer_fingerprint(payload: dict[str, Any], required_skills: list[str]) -> str:
    raw = normalize_text(payload.get("fingerprint"), "")
    allowed = set(FINGERPRINTS.values())
    if raw in allowed:
        return raw

    text = " ".join(
        [
            normalize_text(payload.get("role_archetype"), ""),
            normalize_text(payload.get("role_title"), ""),
            " ".join(required_skills),
        ]
    ).casefold()
    technical_depth = clamp_score(payload.get("technical_depth"))
    ambiguity = clamp_score(payload.get("ambiguity_tolerance"))
    learning = clamp_score(payload.get("learning_agility"))
    ownership = clamp_score(payload.get("ownership"))

    if ambiguity >= 80 and technical_depth >= 75:
        return FINGERPRINTS["high_ambiguity_specialist"]
    if any(word in text for word in ("research", "scientist", "nlp", "ml", "machine learning")) and any(
        word in text for word in ("build", "engineer", "product")
    ):
        return FINGERPRINTS["builder_researcher"]
    if any(word in text for word in ("research", "scientist", "experiment", "statistics")) or learning >= 90:
        return FINGERPRINTS["researcher"]
    if any(word in text for word in ("operator", "operations", "stakeholder", "analyst")) or ownership >= 85:
        return FINGERPRINTS["operator"]
    return FINGERPRINTS["builder"]


def normalize_role_dna_payload(payload: dict[str, Any], job_id: str | None = None) -> RoleDNAProfile:
    required_skills = normalize_list(payload.get("required_skills"))
    preferred_skills = normalize_list(payload.get("preferred_skills"))
    all_skills = list(dict.fromkeys([*required_skills, *preferred_skills]))

    normalized = {
        "job_id": job_id,
        "role_title": normalize_text(payload.get("role_title"), "Unspecified Role"),
        "domain": normalize_text(payload.get("domain"), "General"),
        "seniority": normalize_text(payload.get("seniority"), "Unspecified"),
        "role_archetype": normalize_text(payload.get("role_archetype"), "Generalist"),
        "fingerprint": infer_fingerprint(payload, required_skills),
        "required_skills": required_skills,
        "preferred_skills": preferred_skills,
        "skill_importance": normalize_weights(payload.get("skill_importance"), all_skills),
        "weight_distribution": normalize_weights(payload.get("weight_distribution"), list(WEIGHT_FIELDS)),
        "reasoning": normalize_list(payload.get("reasoning")),
    }

    for field in SCORE_FIELDS:
        normalized[field] = clamp_score(payload.get(field), default=75 if field == "confidence" else 50)

    env_payload = payload.get("work_environment")
    if not isinstance(env_payload, dict):
        env_payload = {}
    normalized["work_environment"] = WorkEnvironmentAttributes(
        startup_vs_enterprise=clamp_score(
            env_payload.get("startup_vs_enterprise"),
            normalized["startup_vs_enterprise_environment"],
        ),
        ambiguity_tolerance=clamp_score(env_payload.get("ambiguity_tolerance"), normalized["ambiguity_tolerance"]),
        collaboration=clamp_score(env_payload.get("collaboration"), normalized["collaboration"]),
        ownership=clamp_score(env_payload.get("ownership"), normalized["ownership"]),
        communication=clamp_score(env_payload.get("communication"), normalized["communication"]),
    )

    if not normalized["reasoning"]:
        normalized["reasoning"] = [
            "Role DNA was normalized from structured role requirements.",
            "Scores are clamped to a 0-100 scale for deterministic comparison.",
        ]

    return RoleDNAProfile(**normalized)
