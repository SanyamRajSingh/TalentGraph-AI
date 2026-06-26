export type Score = number;

export type RoleDNA = {
  roleId: string;
  jobId?: string;
  roleTitle: string;
  domain: string;
  seniority: string;
  roleArchetype: string;
  fingerprint: string;
  requiredSkills: string[];
  preferredSkills: string[];
  skillImportance: Record<string, Score>;
  technicalDepth: Score;
  problemSolving: Score;
  communication: Score;
  ownership: Score;
  leadership: Score;
  learningAgility: Score;
  ambiguityTolerance: Score;
  collaboration: Score;
  startupVsEnterpriseEnvironment: Score;
  workEnvironment: Record<string, Score>;
  weightDistribution: Record<string, Score>;
  reasoning: string[];
  confidence: Score;
};

export type CandidateDigitalTwin = {
  candidateId: string;
  resumeId?: string;
  name: string;
  email?: string;
  phone?: string;
  location?: string;
  skills: string[];
  projects: string[];
  experiences: string[];
  certifications: string[];
  achievements: string[];
  domains: string[];
  timeline: Array<{ year: number; event: string }>;
  technicalDepth: Score;
  learningVelocity: Score;
  leadership: Score;
  ownership: Score;
  communication: Score;
  projectComplexity: Score;
  collaboration: Score;
  consistency: Score;
  growthStage: string;
  confidence: Score;
  reasoning: string[];
  generatedAt: string;
  processingTimeMs: number;
  version: string;
};

export type EvaluatorResult = {
  score: Score;
  confidence: Score;
  strengths: string[];
  risks: string[];
  explanation: string;
};

export type EvaluationBundle = {
  evaluationId: string;
  candidateId: string;
  roleId: string;
  technical: EvaluatorResult;
  growth: EvaluatorResult;
  domain: EvaluatorResult;
  culture: EvaluatorResult;
  overallMatch: Score;
  overallConfidence: Score;
};

export type HiringPersona = "startup_founder" | "enterprise_recruiter" | "research_team";

export type RankingSummary = {
  candidateId: string;
  roleId: string;
  rank: number;
  persona: HiringPersona;
  score: Score;
  confidence: Score;
  evaluationId: string;
};

export type GraphNode = {
  id: string;
  label: "Candidate" | "Role" | "Skill" | "Technology" | "Project" | "Company" | "Domain";
  name: string;
  properties: Record<string, string | number | boolean | null>;
};

export type GraphRelationship = {
  sourceId: string;
  targetId: string;
  type: "HAS_SKILL" | "RELATED_TO" | "USES" | "BELONGS_TO" | "REQUIRES" | "WORKED_AT" | "HAS_DOMAIN";
  properties: Record<string, string | number | boolean | null>;
};

export type KnowledgeGraph = {
  graphId: string;
  nodes: GraphNode[];
  relationships: GraphRelationship[];
};

export type SummaryDocument = {
  id: string;
  kind: string;
  ownerId: string;
  text: string;
  metadata: Record<string, string | number | boolean | null>;
};

export type EmbeddingRecord = {
  id: string;
  sourceId: string;
  kind: string;
  text: string;
  vector: number[];
  metadata: Record<string, string | number | boolean | null>;
};

export type EmbeddingCollection = {
  collectionId: string;
  summaries: SummaryDocument[];
  embeddings: EmbeddingRecord[];
};
