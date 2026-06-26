from app.modules.role_dna.normalizer import normalize_role_dna_payload


def test_normalizer_clamps_scores_and_scales_weights() -> None:
    profile = normalize_role_dna_payload(
        {
            "role_title": "Data Scientist",
            "domain": "FinTech",
            "seniority": "Senior",
            "role_archetype": "Analytical Builder",
            "required_skills": ["Python", "Python", "SQL"],
            "preferred_skills": "Machine Learning, Stakeholder Management",
            "technical_depth": 130,
            "problem_solving": 85,
            "communication": -10,
            "ownership": 80,
            "leadership": 60,
            "learning_agility": 95,
            "ambiguity_tolerance": 70,
            "collaboration": 75,
            "startup_vs_enterprise_environment": 65,
            "skill_importance": {"Python": 60, "SQL": 40},
            "weight_distribution": {"technical_depth": 2, "problem_solving": 1},
        },
        job_id="job_123",
    )

    assert profile.job_id == "job_123"
    assert profile.technical_depth == 100
    assert profile.communication == 0
    assert profile.fingerprint
    assert profile.required_skills == ["Python", "SQL"]
    assert "Machine Learning" in profile.preferred_skills
    assert sum(profile.weight_distribution.values()) == 100
    assert sum(profile.skill_importance.values()) == 100


def test_normalizer_adds_reasoning_when_missing() -> None:
    profile = normalize_role_dna_payload(
        {
            "role_title": "Backend Engineer",
            "domain": "General",
            "seniority": "Mid-level",
            "role_archetype": "Systems Builder",
        }
    )

    assert profile.reasoning
    assert profile.confidence == 75
    assert profile.fingerprint == "Builder"
