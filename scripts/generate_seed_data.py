import os
import json
import random

CANDIDATES_DIR = "data/demo/candidates"
JOBS_DIR = "data/demo/jobs"

os.makedirs(CANDIDATES_DIR, exist_ok=True)
os.makedirs(JOBS_DIR, exist_ok=True)

DOMAINS = ["Fintech", "Healthcare", "E-commerce", "EdTech", "SaaS", "Cybersecurity", "Cloud", "AI/ML"]
LEVELS = ["Intern", "Junior", "Mid", "Senior", "Lead"]
ROLES = ["Backend Engineer", "ML Engineer", "Data Scientist", "Product Analyst", "Full Stack Engineer"]

SKILL_POOLS = {
    "Backend Engineer": ["Python", "Go", "Java", "PostgreSQL", "Redis", "Kafka", "Docker", "Kubernetes", "AWS", "gRPC"],
    "ML Engineer": ["Python", "PyTorch", "TensorFlow", "scikit-learn", "MLflow", "CUDA", "FastAPI", "Ray", "Hugging Face"],
    "Data Scientist": ["Python", "R", "SQL", "Pandas", "NumPy", "XGBoost", "Tableau", "A/B Testing", "Stats"],
    "Product Analyst": ["SQL", "Excel", "Tableau", "Looker", "Mixpanel", "Google Analytics", "Python", "Product Sense"],
    "Full Stack Engineer": ["TypeScript", "React", "Next.js", "Node.js", "Express", "Tailwind CSS", "PostgreSQL", "GraphQL", "AWS"]
}

STRENGTHS_POOL = ["Fast Learner", "Strong Communicator", "Deep Technical Expertise", "Product Mindset", "Leadership", "Data-Driven", "Problem Solver"]
WEAKNESSES_POOL = ["Impatience with Process", "Over-engineers solutions", "Requires structured guidance", "Delegation", "Public Speaking", "Context Switching"]
CAREER_TRAJECTORY_POOL = ["Rapid Promotion Track", "Steady Specialist", "Emerging Leader", "Cross-Functional Contributor"]

def generate_candidates():
    count = 1
    for role in ROLES:
        for _ in range(10):
            level = random.choice(LEVELS)
            domain = random.choice(DOMAINS)
            skills = random.sample(SKILL_POOLS[role], k=min(6, len(SKILL_POOLS[role])))
            
            exp_years = {"Intern": 0, "Junior": 1, "Mid": 3, "Senior": 6, "Lead": 10}[level]
            exp_years += random.randint(0, 2)
            
            candidate = {
                "candidate_id": f"seed_cand_{count}",
                "name": f"Candidate {count} ({level} {role})",
                "email": f"cand{count}@example.com",
                "phone": "+15550000000",
                "experience": f"{exp_years} years",
                "skills": skills,
                "projects": [f"Built a scalable system for {domain}", f"Led initiative in {role.lower()}"],
                "domains": [domain],
                "strengths": random.sample(STRENGTHS_POOL, 2),
                "weaknesses": random.sample(WEAKNESSES_POOL, 1),
                "career_trajectory": random.choice(CAREER_TRAJECTORY_POOL),
                "growth_stage": "Builder" if level in ["Senior", "Lead"] else "Explorer",
                "risk_profile": "Low" if exp_years > 3 else "Medium",
                "timeline": [{"event": "Started", "year": "2020", "role": "Engineer"}],
                "technical_depth": min(100, 40 + exp_years * 5 + random.randint(-5, 10)),
                "learning_velocity": random.randint(60, 95),
                "ownership": min(100, 30 + exp_years * 6 + random.randint(-5, 10)),
                "communication": random.randint(50, 95),
            }
            
            with open(os.path.join(CANDIDATES_DIR, f"{candidate['candidate_id']}.json"), "w") as f:
                json.dump(candidate, f, indent=2)
            count += 1

def generate_jobs():
    for i, role in enumerate(ROLES):
        for j, level in enumerate(["Mid", "Senior"]):
            job_id = f"seed_job_{i}_{j}"
            job = {
                "role_id": job_id,
                "role_title": f"{level} {role}",
                "domain": random.choice(DOMAINS),
                "seniority": level,
                "required_skills": random.sample(SKILL_POOLS[role], k=4),
                "description": f"We are looking for a {level} {role} to join our fast-paced startup.",
                "technical_bar": 70 if level == "Mid" else 85,
                "velocity_bar": 75,
                "ownership_bar": 70 if level == "Mid" else 85,
                "communication_bar": 70,
                "mission_critical_skills": random.sample(SKILL_POOLS[role], k=2)
            }
            with open(os.path.join(JOBS_DIR, f"{job_id}.json"), "w") as f:
                json.dump(job, f, indent=2)

if __name__ == "__main__":
    generate_candidates()
    generate_jobs()
    print("Seed data generated.")
