with open('temp_head.tsx', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
skip_twin = False
for i, line in enumerate(lines):
    if line.startswith('type ApiRoleDNA = {'):
        new_lines.append('''type ApiCandidateTwin = {
  candidate_id: string;
  name: string;
  skills: string[];
  timeline: Array<{ year: number; event: string }>;
  email?: string;
  technical_depth: number;
  problem_solving: number;
  ownership: number;
  learning_agility: number;
  communication: number;
  project_complexity: number;
  collaboration: number;
  consistency: number;
  leadership_readiness: number;
  adaptability: number;
  execution_speed: number;
  business_acumen: number;
  growth_stage: string;
  confidence: number;
  reasoning: string[];
};

''')
        new_lines.append(line)
        continue

    if line.startswith('type ApiCandidateTwin = {'):
        skip_twin = True
        continue
    
    if skip_twin:
        if line.startswith('};'):
            skip_twin = False
        continue

    if line.startswith('type EvaluationResponse = { evaluation: ApiEvaluationBundle };'):
        new_lines.append(line)
        new_lines.append('''
type ApiRecommendationResult = {
  candidate_id: string;
  role_id: string;
  label: "STRONG_HIRE" | "HIRE" | "GROWTH_HIRE" | "BORDERLINE" | "NO_HIRE";
  reason: string;
  supporting_evidence: string[];
};

type RecommendResponse = { recommendation: ApiRecommendationResult };

type ApiCopilotDraftResult = {
  subject: string;
  body: string;
};

type CopilotResponse = ApiCopilotDraftResult;
''')
        continue
        
    if line.startswith('type ExplanationResponse = {'):
        new_lines.append(line)
        new_lines.append('''
type ApiDimensionComparison = {
  dimension: string;
  candidate_a_score: number;
  candidate_b_score: number;
  winner: string;
  delta: number;
};

type ApiComparisonMatrix = {
  candidate_a_id: string;
  candidate_b_id: string;
  candidate_a_name: string;
  candidate_b_name: string;
  role_id: string;
  role_title: string;
  dimensions: ApiDimensionComparison[];
  overall_winner: string;
  summary: string;
  recommendation: string;
  skill_overlap: string[];
  a_unique_skills: string[];
  b_unique_skills: string[];
};

type ApiTalentDistribution = {
  growth_stage: string;
  count: number;
};

type ApiSkillFrequency = {
  skill: string;
  count: number;
};

type ApiAnalyticsOverview = {
  total_candidates: number;
  total_roles: number;
  total_evaluations: number;
  average_confidence: number;
  growth_stage_distribution: ApiTalentDistribution[];
  top_skills: ApiSkillFrequency[];
};
''')
        continue

    if line.strip() == '["consistency", "Consistency"]':
        new_lines.append('  ["consistency", "Consistency"],\n')
        new_lines.append('  ["leadership_readiness", "Leadership Readiness"],\n')
        new_lines.append('  ["adaptability", "Adaptability"],\n')
        new_lines.append('  ["execution_speed", "Execution Speed"],\n')
        new_lines.append('  ["business_acumen", "Business Acumen"]\n')
        continue

    new_lines.append(line)

with open('patched1.tsx', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)
print('Patched types!')
