ROLE_DNA_SYSTEM_PROMPT = """You are an expert recruiting strategist.
Extract a deterministic Role DNA profile from the job description.
Return only valid JSON with concise reasoning. Scores must be 0-100."""


def build_role_dna_user_prompt(job_description: str) -> str:
    return f"""Analyze this job description and return JSON with:
role_title, domain, seniority, role_archetype, required_skills, preferred_skills,
skill_importance, technical_depth, problem_solving, communication, ownership,
leadership, learning_agility, ambiguity_tolerance, collaboration,
startup_vs_enterprise_environment, weight_distribution, work_environment,
reasoning, confidence.

Job description:
{job_description}"""
