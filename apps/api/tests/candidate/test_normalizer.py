from app.domain.candidate_twin import GrowthStage
from app.modules.candidates.normalizer import build_timeline, clamp_score, infer_growth_stage


def test_clamp_score_normalizes_to_integer_range() -> None:
    assert clamp_score(120) == 100
    assert clamp_score(-5) == 0
    assert clamp_score("72.5") == 72
    assert clamp_score("bad", default=44) == 44


def test_timeline_generation_is_deterministic() -> None:
    timeline = build_timeline(
        "2024 Built ML Project\n2023 Learned Python",
        {
            "years": [2024, 2023, 2024],
            "skills": ["Python"],
            "projects": ["Built ML Project"],
        },
    )

    assert [entry.year for entry in timeline] == [2023, 2024]
    assert timeline[0].event == "Built foundation in Python"
    assert timeline[1].event == "Built ML Project"


def test_growth_stage_inference_returns_single_stage() -> None:
    stage = infer_growth_stage(
        {
            "technical_depth": 88,
            "learning_velocity": 70,
            "leadership": 40,
            "ownership": 60,
            "communication": 60,
            "project_complexity": 80,
            "collaboration": 50,
            "consistency": 70,
            "confidence": 80,
        },
        skills=["Python", "Machine Learning"],
        projects=["Built model"],
        domains=["Machine Learning"],
    )

    assert stage in GrowthStage
    assert stage == GrowthStage.RESEARCHER
