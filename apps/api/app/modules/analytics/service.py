from collections import Counter
from app.domain.analytics import AnalyticsOverview, TalentDistribution, SkillFrequency
from app.repositories import CandidateRepository, RoleDNARepository, EvaluationRepository

class AnalyticsService:
    def __init__(
        self,
        candidate_repository: CandidateRepository,
        role_repository: RoleDNARepository,
        evaluation_repository: EvaluationRepository,
    ) -> None:
        self.candidate_repository = candidate_repository
        self.role_repository = role_repository
        self.evaluation_repository = evaluation_repository

    def get_overview(self) -> AnalyticsOverview:
        candidates = self.candidate_repository.list_candidates()
        roles = self.role_repository.list_role_dna()
        
        evaluations = []
        for role in roles:
            evaluations.extend(self.evaluation_repository.list_by_role_id(role.role_id))
            
        total_evaluations = len(evaluations)
        average_confidence = 0.0
        if total_evaluations > 0:
            average_confidence = sum(e.overall_confidence for e in evaluations) / total_evaluations
            
        growth_stages = Counter(c.growth_stage for c in candidates if c.growth_stage)
        stage_dist = [
            TalentDistribution(growth_stage=stage, count=count)
            for stage, count in growth_stages.most_common()
        ]
        
        skills = Counter()
        for c in candidates:
            if c.skills:
                for skill in c.skills:
                    skills[skill.lower()] += 1
                    
        top_skills = [
            SkillFrequency(skill=skill.title(), count=count)
            for skill, count in skills.most_common(10)
        ]
        
        return AnalyticsOverview(
            total_candidates=len(candidates),
            total_roles=len(roles),
            total_evaluations=total_evaluations,
            average_confidence=round(average_confidence, 1),
            growth_stage_distribution=stage_dist,
            top_skills=top_skills,
        )
