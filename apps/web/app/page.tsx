"use client";

import { FormEvent, useMemo, useState } from "react";
import type { ReactNode } from "react";
import { Brain, BriefcaseBusiness, ClipboardCheck, Download, FileText, GitBranch, Layers3, Lightbulb, ListOrdered, Loader2, Sparkles, UserRound } from "lucide-react";

type ApiRoleDNA = {
  role_id: string;
  role_title: string;
  role_archetype: string;
  fingerprint: string;
  required_skills: string[];
  preferred_skills: string[];
  skill_importance: Record<string, number>;
  technical_depth: number;
  problem_solving: number;
  communication: number;
  ownership: number;
  leadership: number;
  learning_agility: number;
  collaboration: number;
  reasoning: string[];
  confidence: number;
};

type ApiCandidateTwin = {
  candidate_id: string;
  resume_id?: string;
  name: string;
  email?: string;
  phone?: string;
  location?: string;
  skills: string[];
  projects: string[];
  experiences: string[];
  domains: string[];
  timeline: Array<{ year: number; event: string }>;
  technical_depth: number;
  learning_velocity: number;
  leadership: number;
  ownership: number;
  communication: number;
  project_complexity: number;
  collaboration: number;
  consistency: number;
  growth_stage: string;
  confidence: number;
  reasoning: string[];
};

type RoleDNAResponse = { role_dna: ApiRoleDNA };
type CandidateTwinResponse = { twin: ApiCandidateTwin };

type ApiGraph = {
  graph_id: string;
  nodes: Array<{ id: string; label: string; name: string }>;
  relationships: Array<{ source_id: string; target_id: string; type: string }>;
};

type ApiEmbeddingCollection = {
  collection_id: string;
  summaries: Array<{ id: string; kind: string; owner_id: string; text: string; metadata: Record<string, unknown> }>;
  embeddings: Array<{ id: string; source_id: string; kind: string; vector: number[]; metadata: Record<string, unknown> }>;
};

type GraphResponse = { graph: ApiGraph };
type EmbeddingResponse = { collection: ApiEmbeddingCollection };

type ApiEvaluatorResult = {
  score: number;
  confidence: number;
  strengths: string[];
  risks: string[];
};

type ApiEvaluationBundle = {
  evaluation_id: string;
  candidate_id: string;
  role_id: string;
  technical: ApiEvaluatorResult;
  growth: ApiEvaluatorResult;
  domain: ApiEvaluatorResult;
  culture: ApiEvaluatorResult;
  overall_match: number;
  overall_confidence: number;
};

type EvaluationResponse = { evaluation: ApiEvaluationBundle };

type HiringPersona = "startup_founder" | "enterprise_recruiter" | "research_team";

type ApiRankingResult = {
  candidate_id: string;
  role_id: string;
  rank: number;
  persona: HiringPersona;
  score: number;
  confidence: number;
  evaluation_id: string;
};

type RankingResponse = {
  role_id: string;
  persona: string;
  rankings: ApiRankingResult[];
};

type ApiExplanationProfile = {
  candidate_id: string;
  role_id: string;
  ranking_position: number;
  strengths: string[];
  risks: string[];
  reasoning: string[];
  counterfactuals: string[];
  generated_at: string;
};

type ExplanationResponse = {
  candidate_id: string;
  role_id: string;
  explanation: ApiExplanationProfile;
};

const personaLabels: Record<HiringPersona, string> = {
  startup_founder: "Startup Founder",
  enterprise_recruiter: "Enterprise Recruiter",
  research_team: "Research Team"
};

const defaultJobDescription = `We are hiring a Senior Data Scientist for a fintech product team.
The role owns ML models for transaction intelligence, partners with product and engineering,
uses Python, SQL, statistics, machine learning, and experimentation, and needs strong ownership
in an ambiguous startup environment.`;

const defaultResume = `# Nikhil Mehta
Email: nikhil.mehta@example.com
Phone: +91 99887 76655
Location: Pune, India

## Skills
- Python
- SQL
- Machine Learning
- NLP
- Docker
- AWS

## Projects
- 2022 Built a churn prediction model using Python, SQL, and machine learning.
- 2023 Created an NLP classifier and documented model behavior for stakeholders.
- 2024 Shipped model monitoring pipeline on AWS with Docker.

## Experience
- 2023 Machine Learning Engineer at DataBridge, owned model training pipelines.
- 2024 Led deployment improvements with platform engineers.`;

const roleScores: Array<[keyof ApiRoleDNA, string]> = [
  ["technical_depth", "Technical Depth"],
  ["problem_solving", "Problem Solving"],
  ["ownership", "Ownership"],
  ["learning_agility", "Learning Agility"],
  ["communication", "Communication"],
  ["collaboration", "Collaboration"]
];

const twinScores: Array<[keyof ApiCandidateTwin, string]> = [
  ["technical_depth", "Technical Depth"],
  ["learning_velocity", "Learning Velocity"],
  ["ownership", "Ownership"],
  ["project_complexity", "Project Complexity"],
  ["communication", "Communication"],
  ["consistency", "Consistency"]
];

export default function Home() {
  const [jobDescription, setJobDescription] = useState(defaultJobDescription);
  const [resumeText, setResumeText] = useState(defaultResume);
  const [roleDNA, setRoleDNA] = useState<ApiRoleDNA | null>(null);
  const [candidateTwin, setCandidateTwin] = useState<ApiCandidateTwin | null>(null);
  const [candidateTwins, setCandidateTwins] = useState<ApiCandidateTwin[]>([]);
  const [graph, setGraph] = useState<ApiGraph | null>(null);
  const [embeddingCollection, setEmbeddingCollection] = useState<ApiEmbeddingCollection | null>(null);
  const [evaluation, setEvaluation] = useState<ApiEvaluationBundle | null>(null);
  const [rankings, setRankings] = useState<ApiRankingResult[]>([]);
  const [explanation, setExplanation] = useState<ApiExplanationProfile | null>(null);
  const [persona, setPersona] = useState<HiringPersona>("startup_founder");
  const [roleLoading, setRoleLoading] = useState(false);
  const [candidateLoading, setCandidateLoading] = useState(false);
  const [graphLoading, setGraphLoading] = useState(false);
  const [embeddingLoading, setEmbeddingLoading] = useState(false);
  const [evaluationLoading, setEvaluationLoading] = useState(false);
  const [rankingLoading, setRankingLoading] = useState(false);
  const [explanationLoading, setExplanationLoading] = useState(false);
  const [exportLoading, setExportLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const apiBaseUrl = useMemo(() => process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000", []);
  const currentRanking = useMemo(
    () => rankings.find((ranking) => ranking.candidate_id === candidateTwin?.candidate_id) ?? null,
    [candidateTwin?.candidate_id, rankings]
  );
  const completedSteps = [
    Boolean(roleDNA),
    candidateTwins.length > 0,
    Boolean(evaluation),
    rankings.length > 0,
    Boolean(explanation)
  ];

  async function handleRoleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setRoleLoading(true);
    setError(null);
    try {
      const response = await fetch(`${apiBaseUrl}/api/v1/generate-role-dna`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ job_description: jobDescription })
      });
      if (!response.ok) throw new Error(`Role DNA generation failed with status ${response.status}`);
      const payload = (await response.json()) as RoleDNAResponse;
      setRoleDNA(payload.role_dna);
      setGraph(null);
      setEmbeddingCollection(null);
      setEvaluation(null);
      setRankings([]);
      setExplanation(null);
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "Unable to generate Role DNA.");
    } finally {
      setRoleLoading(false);
    }
  }

  async function handleCandidateSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setCandidateLoading(true);
    setError(null);
    try {
      const response = await fetch(`${apiBaseUrl}/api/v1/build-digital-twins`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ resume_text: resumeText, source_name: "pasted-resume.md" })
      });
      if (!response.ok) throw new Error(`Candidate twin generation failed with status ${response.status}`);
      const payload = (await response.json()) as CandidateTwinResponse;
      setCandidateTwin(payload.twin);
      setCandidateTwins((items) => [
        ...items.filter((item) => item.candidate_id !== payload.twin.candidate_id),
        payload.twin
      ]);
      setGraph(null);
      setEmbeddingCollection(null);
      setEvaluation(null);
      setRankings([]);
      setExplanation(null);
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "Unable to build Candidate Digital Twin.");
    } finally {
      setCandidateLoading(false);
    }
  }

  async function handleEvaluation() {
    if (!roleDNA || !candidateTwin) return;
    setEvaluationLoading(true);
    setError(null);
    try {
      const response = await fetch(`${apiBaseUrl}/api/v1/evaluate`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          role_id: roleDNA.role_id,
          candidate_id: candidateTwin.candidate_id
        })
      });
      if (!response.ok) throw new Error(`Evaluation failed with status ${response.status}`);
      const payload = (await response.json()) as EvaluationResponse;
      setEvaluation(payload.evaluation);
      setExplanation(null);
      await rankForPersona(persona);
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "Unable to evaluate candidate match.");
    } finally {
      setEvaluationLoading(false);
    }
  }

  async function rankForPersona(selectedPersona: HiringPersona) {
    if (!roleDNA) return;
    setRankingLoading(true);
    setError(null);
    try {
      const response = await fetch(`${apiBaseUrl}/api/v1/rank`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ role_id: roleDNA.role_id, persona: selectedPersona })
      });
      if (!response.ok) throw new Error(`Ranking failed with status ${response.status}`);
      const payload = (await response.json()) as RankingResponse;
      setRankings(payload.rankings);
      setExplanation(null);
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "Unable to rank candidates.");
    } finally {
      setRankingLoading(false);
    }
  }

  async function handlePersonaChange(selectedPersona: HiringPersona) {
    setPersona(selectedPersona);
    setExplanation(null);
    if (evaluation) {
      await rankForPersona(selectedPersona);
    }
  }

  async function handleExplanationGeneration() {
    if (!roleDNA || !candidateTwin || !currentRanking) return;
    setExplanationLoading(true);
    setError(null);
    try {
      const response = await fetch(`${apiBaseUrl}/api/v1/generate-explanations`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          role_id: roleDNA.role_id,
          candidate_id: candidateTwin.candidate_id,
          persona
        })
      });
      if (!response.ok) throw new Error(`Explanation generation failed with status ${response.status}`);
      const payload = (await response.json()) as ExplanationResponse;
      setExplanation(payload.explanation);
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "Unable to generate explanation.");
    } finally {
      setExplanationLoading(false);
    }
  }

  async function handleExportRankings() {
    if (!roleDNA || !rankings.length) return;
    setExportLoading(true);
    setError(null);
    try {
      const response = await fetch(`${apiBaseUrl}/api/v1/export-rankings`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ role_id: roleDNA.role_id, persona })
      });
      if (!response.ok) throw new Error(`Export failed with status ${response.status}`);
      const blob = await response.blob();
      const url = URL.createObjectURL(blob);
      const anchor = document.createElement("a");
      anchor.href = url;
      anchor.download = `talentgraph-rankings-${roleDNA.role_id}.xlsx`;
      anchor.click();
      URL.revokeObjectURL(url);
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "Unable to export rankings.");
    } finally {
      setExportLoading(false);
    }
  }

  async function handleGraphBuild() {
    if (!roleDNA && !candidateTwin) return;
    setGraphLoading(true);
    setError(null);
    try {
      const response = await fetch(`${apiBaseUrl}/api/v1/build-graph`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          role_id: roleDNA?.role_id,
          candidate_id: candidateTwin?.candidate_id
        })
      });
      if (!response.ok) throw new Error(`Graph build failed with status ${response.status}`);
      const payload = (await response.json()) as GraphResponse;
      setGraph(payload.graph);
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "Unable to build graph.");
    } finally {
      setGraphLoading(false);
    }
  }

  async function handleEmbeddingGeneration() {
    if (!roleDNA && !candidateTwin) return;
    setEmbeddingLoading(true);
    setError(null);
    try {
      const response = await fetch(`${apiBaseUrl}/api/v1/generate-embeddings`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          role_id: roleDNA?.role_id,
          candidate_id: candidateTwin?.candidate_id
        })
      });
      if (!response.ok) throw new Error(`Embedding generation failed with status ${response.status}`);
      const payload = (await response.json()) as EmbeddingResponse;
      setEmbeddingCollection(payload.collection);
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "Unable to generate embeddings.");
    } finally {
      setEmbeddingLoading(false);
    }
  }

  return (
    <main className="min-h-screen bg-[#f7f8fb] text-ink">
      <header className="border-b border-gray-200 bg-white">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-5">
          <div>
            <p className="text-sm font-semibold uppercase tracking-wide text-mint">
              Explainable Hiring Intelligence Platform
            </p>
            <h1 className="mt-1 text-3xl font-semibold">TalentGraph AI</h1>
          </div>
          <div className="flex items-center gap-2 rounded border border-gray-200 px-3 py-2 text-sm text-graphite">
            <Sparkles className="h-4 w-4 text-amber" aria-hidden="true" />
            Demo Modules 1-7
          </div>
        </div>
      </header>

      <section className="mx-auto max-w-7xl px-6 py-6">
        <ProgressSteps completed={completedSteps} />
      </section>

      <section className="mx-auto grid max-w-7xl gap-6 px-6 pb-8 lg:grid-cols-2">
        <ModulePanel
          eyebrow="Step 1"
          title="Generate Role DNA"
          icon={<BriefcaseBusiness className="h-6 w-6 text-signal" aria-hidden="true" />}
          form={
            <form onSubmit={handleRoleSubmit}>
              <Textarea
                id="job-description"
                label="Job description"
                value={jobDescription}
                onChange={setJobDescription}
              />
              <SubmitButton loading={roleLoading} disabled={!jobDescription.trim()} label="Generate Role DNA" />
            </form>
          }
        >
          {roleDNA ? (
            <div className="space-y-5">
              <div className="grid gap-3 sm:grid-cols-2">
                <Summary label="Role" value={roleDNA.role_title} />
                <Summary label="Fingerprint" value={roleDNA.fingerprint} />
                <Summary label="Archetype" value={roleDNA.role_archetype} />
                <Summary label="Confidence" value={`${roleDNA.confidence}%`} />
              </div>
              <RadarChart role={roleDNA} />
              <ScoreList rows={roleScores} source={roleDNA} />
              <SkillList title="Required Skills" skills={roleDNA.required_skills} />
              <ReasoningList items={roleDNA.reasoning} />
            </div>
          ) : (
            <EmptyState text="Generate Role DNA to inspect role archetype, weighted skills, and reasoning." />
          )}
        </ModulePanel>

        <ModulePanel
          eyebrow="Step 2"
          title="Generate Candidate Twins"
          icon={<FileText className="h-6 w-6 text-mint" aria-hidden="true" />}
          form={
            <form onSubmit={handleCandidateSubmit}>
              <Textarea id="resume-text" label="Resume text" value={resumeText} onChange={setResumeText} />
              <SubmitButton loading={candidateLoading} disabled={!resumeText.trim()} label="Build Digital Twin" />
            </form>
          }
        >
          {candidateTwin ? (
            <div className="space-y-5">
              <div className="grid gap-3 sm:grid-cols-2">
                <Summary label="Candidate" value={candidateTwin.name} />
                <Summary label="Growth Stage" value={candidateTwin.growth_stage} />
                <Summary label="Twins Built" value={String(candidateTwins.length)} />
                <Summary label="Email" value={candidateTwin.email ?? "Not found"} />
              </div>
              <MetricCards rows={twinScores} source={candidateTwin} />
              <SkillList title="Skills" skills={candidateTwin.skills} />
              <Timeline entries={candidateTwin.timeline} />
              <ReasoningList items={candidateTwin.reasoning} />
            </div>
          ) : (
            <EmptyState text="Build a Candidate Digital Twin to inspect skills, timeline, growth stage, and reasoning." />
          )}
        </ModulePanel>
      </section>

      <section className="mx-auto max-w-7xl px-6 pb-8">
        <ModulePanel
          eyebrow="Step 3"
          title="Evaluate Candidates"
          icon={<ClipboardCheck className="h-6 w-6 text-signal" aria-hidden="true" />}
          form={
            <button
              type="button"
              onClick={handleEvaluation}
              disabled={evaluationLoading || !roleDNA || !candidateTwin}
              className="inline-flex h-11 items-center justify-center gap-2 rounded bg-signal px-4 text-sm font-semibold text-white disabled:cursor-not-allowed disabled:bg-gray-400"
            >
              {evaluationLoading ? <Loader2 className="h-4 w-4 animate-spin" aria-hidden="true" /> : <ClipboardCheck className="h-4 w-4" aria-hidden="true" />}
              Evaluate Match
            </button>
          }
        >
          {evaluation ? (
            <div className="space-y-5">
              <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-6">
                <Summary label="Overall Match" value={`${evaluation.overall_match}`} />
                <Summary label="Confidence" value={`${evaluation.overall_confidence}`} />
                <Summary label="Technical" value={`${evaluation.technical.score}`} />
                <Summary label="Growth" value={`${evaluation.growth.score}`} />
                <Summary label="Domain" value={`${evaluation.domain.score}`} />
                <Summary label="Culture" value={`${evaluation.culture.score}`} />
              </div>
              <div className="grid gap-4 lg:grid-cols-4">
                <EvaluatorCard title="Technical" result={evaluation.technical} />
                <EvaluatorCard title="Growth" result={evaluation.growth} />
                <EvaluatorCard title="Domain" result={evaluation.domain} />
                <EvaluatorCard title="Culture" result={evaluation.culture} />
              </div>
            </div>
          ) : (
            <EmptyState text="Generate a Role DNA profile and Candidate Twin, then evaluate deterministic match dimensions." />
          )}
        </ModulePanel>
      </section>

      <section className="mx-auto max-w-7xl px-6 pb-8">
        <ModulePanel
          eyebrow="Step 4"
          title="Rank Candidates"
          icon={<ListOrdered className="h-6 w-6 text-amber" aria-hidden="true" />}
          form={
            <div className="flex flex-wrap items-center gap-3">
              <label htmlFor="persona" className="text-sm font-medium text-graphite">
                Persona
              </label>
              <select
                id="persona"
                value={persona}
                onChange={(event) => void handlePersonaChange(event.target.value as HiringPersona)}
                className="h-10 rounded border border-gray-300 bg-white px-3 text-sm outline-none focus:border-signal focus:ring-2 focus:ring-blue-100"
              >
                {Object.entries(personaLabels).map(([value, label]) => (
                  <option key={value} value={value}>
                    {label}
                  </option>
                ))}
              </select>
              <button
                type="button"
                onClick={() => void rankForPersona(persona)}
                disabled={rankingLoading || !evaluation}
                className="inline-flex h-10 items-center justify-center gap-2 rounded bg-signal px-4 text-sm font-semibold text-white disabled:cursor-not-allowed disabled:bg-gray-400"
              >
                {rankingLoading ? <Loader2 className="h-4 w-4 animate-spin" aria-hidden="true" /> : <ListOrdered className="h-4 w-4" aria-hidden="true" />}
                Rank
              </button>
              <button
                type="button"
                onClick={handleExportRankings}
                disabled={exportLoading || !rankings.length}
                className="inline-flex h-10 items-center justify-center gap-2 rounded border border-gray-300 bg-white px-4 text-sm font-semibold text-ink disabled:cursor-not-allowed disabled:text-gray-400"
              >
                {exportLoading ? <Loader2 className="h-4 w-4 animate-spin" aria-hidden="true" /> : <Download className="h-4 w-4" aria-hidden="true" />}
                XLSX
              </button>
            </div>
          }
        >
          {rankings.length ? (
            <div className="overflow-auto">
              <table className="w-full border-collapse text-left text-sm">
                <thead>
                  <tr className="border-b border-gray-200 text-xs uppercase tracking-wide text-graphite">
                    <th className="py-2 pr-3">Rank</th>
                    <th className="py-2 pr-3">Candidate</th>
                    <th className="py-2 pr-3">Score</th>
                    <th className="py-2 pr-3">Confidence</th>
                  </tr>
                </thead>
                <tbody>
                  {rankings.map((ranking) => (
                    <tr key={`${ranking.persona}-${ranking.candidate_id}`} className="border-b border-gray-100">
                      <td className="py-3 pr-3 font-semibold">{ranking.rank}</td>
                      <td className="py-3 pr-3">{candidateTwin?.candidate_id === ranking.candidate_id ? candidateTwin.name : ranking.candidate_id}</td>
                      <td className="py-3 pr-3">{ranking.score}</td>
                      <td className="py-3 pr-3">{ranking.confidence}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : (
            <EmptyState text="Evaluate at least one candidate, then rank using a hiring persona." />
          )}
        </ModulePanel>
      </section>

      <section className="mx-auto max-w-7xl px-6 pb-8">
        <ModulePanel
          eyebrow="Step 5"
          title="View Explanations"
          icon={<Lightbulb className="h-6 w-6 text-mint" aria-hidden="true" />}
          form={
            <button
              type="button"
              onClick={handleExplanationGeneration}
              disabled={explanationLoading || !roleDNA || !candidateTwin || !evaluation || !currentRanking}
              className="inline-flex h-11 items-center justify-center gap-2 rounded bg-signal px-4 text-sm font-semibold text-white disabled:cursor-not-allowed disabled:bg-gray-400"
            >
              {explanationLoading ? <Loader2 className="h-4 w-4 animate-spin" aria-hidden="true" /> : <Lightbulb className="h-4 w-4" aria-hidden="true" />}
              Generate Explanation
            </button>
          }
        >
          {explanation && currentRanking ? (
            <div className="space-y-5">
              <div className="grid gap-3 sm:grid-cols-3">
                <Summary label="Rank" value={`#${explanation.ranking_position}`} />
                <Summary label="Score" value={String(currentRanking.score)} />
                <Summary label="Candidate" value={candidateTwin?.name ?? explanation.candidate_id} />
              </div>
              <div className="grid gap-4 lg:grid-cols-2">
                <InsightList title="Strengths" items={explanation.strengths} fallback="No major strength signal." />
                <InsightList title="Risks" items={explanation.risks} fallback="No major risk signal." />
              </div>
              <InsightList title="Why This Candidate" items={explanation.reasoning} fallback="No reasoning generated." />
              <CounterfactualCards items={explanation.counterfactuals} />
            </div>
          ) : (
            <EmptyState text="Evaluate and rank the candidate, then generate strengths, risks, reasoning, and improvement suggestions." />
          )}
        </ModulePanel>
      </section>

      <section className="mx-auto grid max-w-7xl gap-6 px-6 pb-8 lg:grid-cols-2">
        <ModulePanel
          eyebrow="Semantic Foundation"
          title="Knowledge Graph"
          icon={<GitBranch className="h-6 w-6 text-amber" aria-hidden="true" />}
          form={
            <button
              type="button"
              onClick={handleGraphBuild}
              disabled={graphLoading || (!roleDNA && !candidateTwin)}
              className="inline-flex h-11 items-center justify-center gap-2 rounded bg-signal px-4 text-sm font-semibold text-white disabled:cursor-not-allowed disabled:bg-gray-400"
            >
              {graphLoading ? <Loader2 className="h-4 w-4 animate-spin" aria-hidden="true" /> : <GitBranch className="h-4 w-4" aria-hidden="true" />}
              Build Graph
            </button>
          }
        >
          {graph ? (
            <div className="space-y-5">
              <div className="grid gap-3 sm:grid-cols-3">
                <Summary label="Graph" value={graph.graph_id} />
                <Summary label="Nodes" value={String(graph.nodes.length)} />
                <Summary label="Relationships" value={String(graph.relationships.length)} />
              </div>
              <GraphList title="Nodes" items={graph.nodes.map((node) => `${node.label}: ${node.name}`)} />
              <GraphList
                title="Relationships"
                items={graph.relationships.map((relationship) => `${relationship.source_id} ${relationship.type} ${relationship.target_id}`)}
              />
            </div>
          ) : (
            <EmptyState text="Generate Role DNA or a Candidate Twin, then build a semantic graph of nodes and relationships." />
          )}
        </ModulePanel>

        <ModulePanel
          eyebrow="Semantic Foundation"
          title="Embedding Inspection"
          icon={<Layers3 className="h-6 w-6 text-mint" aria-hidden="true" />}
          form={
            <button
              type="button"
              onClick={handleEmbeddingGeneration}
              disabled={embeddingLoading || (!roleDNA && !candidateTwin)}
              className="inline-flex h-11 items-center justify-center gap-2 rounded bg-signal px-4 text-sm font-semibold text-white disabled:cursor-not-allowed disabled:bg-gray-400"
            >
              {embeddingLoading ? <Loader2 className="h-4 w-4 animate-spin" aria-hidden="true" /> : <Layers3 className="h-4 w-4" aria-hidden="true" />}
              Generate Embeddings
            </button>
          }
        >
          {embeddingCollection ? (
            <div className="space-y-5">
              <div className="grid gap-3 sm:grid-cols-3">
                <Summary label="Collection" value={embeddingCollection.collection_id} />
                <Summary label="Summaries" value={String(embeddingCollection.summaries.length)} />
                <Summary label="Vectors" value={String(embeddingCollection.embeddings.length)} />
              </div>
              <div>
                <h3 className="text-sm font-semibold uppercase tracking-wide text-graphite">Summaries</h3>
                <ul className="mt-3 space-y-2">
                  {embeddingCollection.summaries.map((summary) => (
                    <li key={summary.id} className="rounded border border-gray-200 p-3 text-sm leading-6">
                      <span className="font-semibold">{summary.kind}</span>: {summary.text}
                    </li>
                  ))}
                </ul>
              </div>
              <GraphList
                title="Embedding Metadata"
                items={embeddingCollection.embeddings.map(
                  (embedding) => `${embedding.kind} | dimensions ${embedding.vector.length} | ${embedding.source_id}`
                )}
              />
            </div>
          ) : (
            <EmptyState text="Generate deterministic summary, skill, and project embeddings for inspection." />
          )}
        </ModulePanel>
      </section>

      {error ? (
        <div className="mx-auto mb-8 max-w-7xl px-6">
          <p className="rounded border border-red-200 bg-red-50 p-3 text-sm font-medium text-red-700">{error}</p>
        </div>
      ) : null}
    </main>
  );
}

function ModulePanel({
  eyebrow,
  title,
  icon,
  form,
  children
}: {
  eyebrow?: string;
  title: string;
  icon: ReactNode;
  form: ReactNode;
  children: ReactNode;
}) {
  return (
    <section className="rounded border border-gray-200 bg-white p-6">
      <div className="flex items-center gap-3">
        {icon}
        <div>
          {eyebrow ? <p className="text-xs font-semibold uppercase tracking-wide text-graphite">{eyebrow}</p> : null}
          <h2 className="text-xl font-semibold">{title}</h2>
        </div>
      </div>
      <div className="mt-5">{form}</div>
      <div className="mt-6 border-t border-gray-100 pt-6">{children}</div>
    </section>
  );
}

function ProgressSteps({ completed }: { completed: boolean[] }) {
  const labels = ["Role DNA", "Candidate Twins", "Evaluate", "Rank", "Explain"];
  return (
    <div className="grid gap-3 rounded border border-gray-200 bg-white p-4 sm:grid-cols-5">
      {labels.map((label, index) => {
        const isComplete = completed[index];
        return (
          <div key={label} className="flex items-center gap-3">
            <div
              className={`flex h-8 w-8 shrink-0 items-center justify-center rounded-full text-sm font-semibold ${
                isComplete ? "bg-mint text-white" : "bg-gray-100 text-graphite"
              }`}
            >
              {index + 1}
            </div>
            <div>
              <p className="text-sm font-semibold">{label}</p>
              <p className="text-xs text-graphite">{isComplete ? "Complete" : "Pending"}</p>
            </div>
          </div>
        );
      })}
    </div>
  );
}

function Textarea({
  id,
  label,
  value,
  onChange
}: {
  id: string;
  label: string;
  value: string;
  onChange: (value: string) => void;
}) {
  return (
    <>
      <label htmlFor={id} className="block text-sm font-medium text-graphite">
        {label}
      </label>
      <textarea
        id={id}
        value={value}
        onChange={(event) => onChange(event.target.value)}
        className="mt-2 min-h-[260px] w-full resize-y rounded border border-gray-300 bg-white p-4 text-sm leading-6 outline-none focus:border-signal focus:ring-2 focus:ring-blue-100"
      />
    </>
  );
}

function SubmitButton({ loading, disabled, label }: { loading: boolean; disabled: boolean; label: string }) {
  return (
    <button
      type="submit"
      disabled={loading || disabled}
      className="mt-4 inline-flex h-11 items-center justify-center gap-2 rounded bg-signal px-4 text-sm font-semibold text-white disabled:cursor-not-allowed disabled:bg-gray-400"
    >
      {loading ? <Loader2 className="h-4 w-4 animate-spin" aria-hidden="true" /> : <Brain className="h-4 w-4" aria-hidden="true" />}
      {label}
    </button>
  );
}

function Summary({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded border border-gray-200 p-4">
      <p className="text-xs font-semibold uppercase tracking-wide text-graphite">{label}</p>
      <p className="mt-2 text-base font-semibold">{value}</p>
    </div>
  );
}

function ScoreList<T extends Record<string, unknown>>({ rows, source }: { rows: Array<[keyof T, string]>; source: T }) {
  return (
    <div className="space-y-3">
      {rows.map(([key, label]) => (
        <ScoreBar key={String(key)} label={label} value={Number(source[key])} />
      ))}
    </div>
  );
}

function ScoreBar({ label, value }: { label: string; value: number }) {
  return (
    <div>
      <div className="flex items-center justify-between text-sm">
        <span className="font-medium">{label}</span>
        <span className="text-graphite">{value}</span>
      </div>
      <div className="mt-1 h-2 rounded bg-gray-100">
        <div className="h-2 rounded bg-mint" style={{ width: `${Math.max(0, Math.min(100, value))}%` }} />
      </div>
    </div>
  );
}

function RadarChart({ role }: { role: ApiRoleDNA }) {
  const metrics = [
    ["Technical", role.technical_depth],
    ["Problem", role.problem_solving],
    ["Ownership", role.ownership],
    ["Learning", role.learning_agility],
    ["Comms", role.communication],
    ["Collab", role.collaboration]
  ] as const;
  const center = 90;
  const radius = 58;
  const points = metrics
    .map(([, value], index) => {
      const angle = -Math.PI / 2 + (index * 2 * Math.PI) / metrics.length;
      const scaled = radius * (value / 100);
      return `${center + scaled * Math.cos(angle)},${center + scaled * Math.sin(angle)}`;
    })
    .join(" ");

  return (
    <div>
      <h3 className="text-sm font-semibold uppercase tracking-wide text-graphite">Role Radar</h3>
      <div className="mt-3 grid gap-4 md:grid-cols-[220px_1fr]">
        <svg viewBox="0 0 180 180" className="h-52 w-full max-w-56">
          {[0.35, 0.7, 1].map((scale) => {
            const ring = metrics
              .map(([,], index) => {
                const angle = -Math.PI / 2 + (index * 2 * Math.PI) / metrics.length;
                const scaled = radius * scale;
                return `${center + scaled * Math.cos(angle)},${center + scaled * Math.sin(angle)}`;
              })
              .join(" ");
            return <polygon key={scale} points={ring} fill="none" stroke="#d1d5db" strokeWidth="1" />;
          })}
          {metrics.map(([label], index) => {
            const angle = -Math.PI / 2 + (index * 2 * Math.PI) / metrics.length;
            const x = center + (radius + 22) * Math.cos(angle);
            const y = center + (radius + 22) * Math.sin(angle);
            return (
              <text key={label} x={x} y={y} textAnchor="middle" dominantBaseline="middle" className="fill-gray-600 text-[8px]">
                {label}
              </text>
            );
          })}
          <polygon points={points} fill="#14b8a633" stroke="#0f766e" strokeWidth="2" />
        </svg>
        <div className="grid gap-2 sm:grid-cols-2">
          {metrics.map(([label, value]) => (
            <Summary key={label} label={label} value={String(value)} />
          ))}
        </div>
      </div>
    </div>
  );
}

function MetricCards<T extends Record<string, unknown>>({ rows, source }: { rows: Array<[keyof T, string]>; source: T }) {
  return (
    <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
      {rows.map(([key, label]) => (
        <Summary key={String(key)} label={label} value={String(Number(source[key]))} />
      ))}
    </div>
  );
}

function SkillList({ title, skills }: { title: string; skills: string[] }) {
  return (
    <div>
      <h3 className="text-sm font-semibold uppercase tracking-wide text-graphite">{title}</h3>
      <div className="mt-3 flex flex-wrap gap-2">
        {skills.length ? (
          skills.map((skill) => (
            <span key={skill} className="rounded border border-gray-200 px-3 py-1 text-sm">
              {skill}
            </span>
          ))
        ) : (
          <span className="text-sm text-graphite">No skills extracted</span>
        )}
      </div>
    </div>
  );
}

function Timeline({ entries }: { entries: Array<{ year: number; event: string }> }) {
  return (
    <div>
      <h3 className="text-sm font-semibold uppercase tracking-wide text-graphite">Timeline</h3>
      <ol className="mt-3 space-y-2">
        {entries.map((entry) => (
          <li key={`${entry.year}-${entry.event}`} className="flex gap-3 rounded border border-gray-200 p-3 text-sm">
            <span className="font-semibold text-signal">{entry.year}</span>
            <span>{entry.event}</span>
          </li>
        ))}
      </ol>
    </div>
  );
}

function GraphList({ title, items }: { title: string; items: string[] }) {
  return (
    <div>
      <h3 className="text-sm font-semibold uppercase tracking-wide text-graphite">{title}</h3>
      <ul className="mt-3 max-h-72 space-y-2 overflow-auto">
        {items.map((item) => (
          <li key={item} className="rounded border border-gray-200 p-3 text-sm">
            {item}
          </li>
        ))}
      </ul>
    </div>
  );
}

function ReasoningList({ items }: { items: string[] }) {
  return (
    <div>
      <h3 className="text-sm font-semibold uppercase tracking-wide text-graphite">Reasoning</h3>
      <ul className="mt-3 space-y-2">
        {items.map((item) => (
          <li key={item} className="rounded border border-gray-200 p-3 text-sm leading-6">
            {item}
          </li>
        ))}
      </ul>
    </div>
  );
}

function InsightList({ title, items, fallback }: { title: string; items: string[]; fallback: string }) {
  const visibleItems = items.length ? items : [fallback];
  return (
    <div>
      <h3 className="text-sm font-semibold uppercase tracking-wide text-graphite">{title}</h3>
      <ul className="mt-3 space-y-2">
        {visibleItems.map((item) => (
          <li key={item} className="rounded border border-gray-200 p-3 text-sm leading-6">
            {item}
          </li>
        ))}
      </ul>
    </div>
  );
}

function CounterfactualCards({ items }: { items: string[] }) {
  const visibleItems = items.length ? items : ["No counterfactuals generated."];
  return (
    <div>
      <h3 className="text-sm font-semibold uppercase tracking-wide text-graphite">How To Improve</h3>
      <div className="mt-3 grid gap-3 lg:grid-cols-3">
        {visibleItems.map((item, index) => (
          <div key={item} className="rounded border border-mint/30 bg-teal-50 p-4">
            <p className="text-xs font-semibold uppercase tracking-wide text-mint">Counterfactual {index + 1}</p>
            <p className="mt-2 text-sm leading-6">{item}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

function EvaluatorCard({ title, result }: { title: string; result: ApiEvaluatorResult }) {
  return (
    <div className="rounded border border-gray-200 p-4">
      <div className="flex items-center justify-between">
        <h3 className="font-semibold">{title}</h3>
        <span className="text-sm font-semibold text-signal">{result.score}</span>
      </div>
      <p className="mt-1 text-sm text-graphite">Confidence {result.confidence}</p>
      <h4 className="mt-4 text-xs font-semibold uppercase tracking-wide text-graphite">Strengths</h4>
      <ul className="mt-2 space-y-2">
        {(result.strengths.length ? result.strengths : ["No major strength signal."]).map((item) => (
          <li key={item} className="text-sm leading-5">
            {item}
          </li>
        ))}
      </ul>
      <h4 className="mt-4 text-xs font-semibold uppercase tracking-wide text-graphite">Risks</h4>
      <ul className="mt-2 space-y-2">
        {(result.risks.length ? result.risks : ["No major risk signal."]).map((item) => (
          <li key={item} className="text-sm leading-5">
            {item}
          </li>
        ))}
      </ul>
    </div>
  );
}

function EmptyState({ text }: { text: string }) {
  return (
    <div className="flex min-h-[220px] items-center justify-center rounded border border-dashed border-gray-300 p-6 text-center text-graphite">
      <div>
        <UserRound className="mx-auto mb-3 h-6 w-6 text-gray-400" aria-hidden="true" />
        {text}
      </div>
    </div>
  );
}
