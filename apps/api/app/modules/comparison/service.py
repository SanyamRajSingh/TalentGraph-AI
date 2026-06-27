from app.domain.candidate_twin import CandidateDigitalTwin
from app.domain.comparison import ComparisonMatrix, DimensionComparison
from app.domain.role_dna import RoleDNAProfile

# Ordered list of dimensions to compare (attr_name, display_label)
COMPARISON_DIMENSIONS = [
    ("technical_depth",      "Technical Depth"),
    ("learning_velocity",    "Learning Velocity"),
    ("ownership",            "Ownership"),
    ("communication",        "Communication"),
    ("leadership",           "Leadership"),
    ("project_complexity",   "Project Complexity"),
    ("collaboration",        "Collaboration"),
    ("consistency",          "Consistency"),
    ("leadership_readiness", "Leadership Readiness"),
    ("adaptability",         "Adaptability"),
    ("execution_speed",      "Execution Speed"),
    ("business_acumen",      "Business Acumen"),
    ("confidence",           "Profile Confidence"),
]


class ComparisonService:
    """Generates a side-by-side comparison matrix for two candidates against a role."""

    def compare(
        self,
        candidate_a: CandidateDigitalTwin,
        candidate_b: CandidateDigitalTwin,
        role: RoleDNAProfile,
    ) -> ComparisonMatrix:
        dimensions = []
        a_wins = 0
        b_wins = 0

        for attr, label in COMPARISON_DIMENSIONS:
            a_val = int(getattr(candidate_a, attr, 50))
            b_val = int(getattr(candidate_b, attr, 50))
            delta = a_val - b_val

            if delta > 2:
                winner = "A"
                a_wins += 1
            elif delta < -2:
                winner = "B"
                b_wins += 1
            else:
                winner = "TIE"

            dimensions.append(DimensionComparison(
                dimension=label,
                candidate_a_score=a_val,
                candidate_b_score=b_val,
                winner=winner,
                delta=delta,
            ))

        # Overall winner
        if a_wins > b_wins:
            overall_winner = "A"
        elif b_wins > a_wins:
            overall_winner = "B"
        else:
            overall_winner = "TIE"

        # Skill analysis
        a_skills = {s.lower() for s in candidate_a.skills}
        b_skills = {s.lower() for s in candidate_b.skills}
        overlap_raw = a_skills & b_skills
        role_req = {s.lower() for s in role.required_skills}

        # Show overlap sorted by role relevance first
        skill_overlap = sorted(overlap_raw, key=lambda s: s in role_req, reverse=True)
        a_unique = sorted(a_skills - b_skills, key=lambda s: s in role_req, reverse=True)
        b_unique = sorted(b_skills - a_skills, key=lambda s: s in role_req, reverse=True)

        # Narrative summary
        winner_name = candidate_a.name if overall_winner == "A" else (candidate_b.name if overall_winner == "B" else "Neither candidate")
        loser_name = candidate_b.name if overall_winner == "A" else (candidate_a.name if overall_winner == "B" else "")

        if overall_winner == "TIE":
            summary = (
                f"{candidate_a.name} and {candidate_b.name} are closely matched for the '{role.role_title}' role, "
                f"each winning {a_wins} dimensions. The decision depends on soft signals and interview performance."
            )
            recommendation = (
                f"Both candidates are comparable fits for '{role.role_title}'. "
                f"Consider {candidate_a.name} for depth on technical dimensions and {candidate_b.name} for broader adaptability."
                if candidate_a.technical_depth != candidate_b.technical_depth
                else f"Conduct final interviews with both {candidate_a.name} and {candidate_b.name} before deciding."
            )
        else:
            summary = (
                f"{winner_name} edges ahead of {loser_name} for the '{role.role_title}' role, "
                f"winning {max(a_wins, b_wins)} of {len(dimensions)} evaluated dimensions."
            )
            recommendation = (
                f"Recommended: {winner_name}. "
                f"{'Strong' if max(a_wins, b_wins) >= 8 else 'Moderate'} advantage in key competency dimensions. "
                f"{loser_name} may be a strong fit for a more junior or specialised variation of this role."
            )

        return ComparisonMatrix(
            candidate_a_id=candidate_a.candidate_id,
            candidate_b_id=candidate_b.candidate_id,
            candidate_a_name=candidate_a.name,
            candidate_b_name=candidate_b.name,
            role_id=role.role_id,
            role_title=role.role_title,
            dimensions=dimensions,
            overall_winner=overall_winner,
            summary=summary,
            recommendation=recommendation,
            skill_overlap=skill_overlap[:10],
            a_unique_skills=a_unique[:10],
            b_unique_skills=b_unique[:10],
        )
