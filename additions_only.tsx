import React, { FormEvent, useCallback, useEffect, useMemo, useRef, useState } from "react";
  leadership_readiness: number;
  adaptability: number;
  execution_speed: number;
  business_acumen: number;
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

  evidence: string[];
  estimations: string[];
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

  ["consistency", "Consistency"],
  ["leadership_readiness", "Leadership Readiness"],
  ["adaptability", "Adaptability"],
  ["execution_speed", "Execution Speed"],
  ["business_acumen", "Business Acumen"]
  const [recommendation, setRecommendation] = useState<ApiRecommendationResult | null>(null);
  const [copilotDraft, setCopilotDraft] = useState<ApiCopilotDraftResult | null>(null);
  const [copilotLoading, setCopilotLoading] = useState(false);
  const [activeTab, setActiveTab] = useState<"workflow" | "library" | "analytics">("workflow");
  const [libraryCandidates, setLibraryCandidates] = useState<ApiCandidateTwin[]>([]);
  const [libraryLoading, setLibraryLoading] = useState(false);
  const [analyticsOverview, setAnalyticsOverview] = useState<ApiAnalyticsOverview | null>(null);
  const [analyticsLoading, setAnalyticsLoading] = useState(false);
  
  // Comparison State
  const [compareCandidateId, setCompareCandidateId] = useState<string>("");
  const [comparisonMatrix, setComparisonMatrix] = useState<ApiComparisonMatrix | null>(null);
  const [comparisonLoading, setComparisonLoading] = useState(false);

  // Batch Upload State
  const [batchJobId, setBatchJobId] = useState<string | null>(null);
  const [batchStatus, setBatchStatus] = useState<any>(null);
  const [batchLoading, setBatchLoading] = useState(false);
  useEffect(() => {
    if (activeTab === "library") {
      fetchLibraryCandidates();
    } else if (activeTab === "analytics") {
      fetchAnalyticsData();
    }
  }, [activeTab]);

  async function fetchAnalyticsData() {
    setAnalyticsLoading(true);
    try {
      const response = await fetch(`${apiBaseUrl}/api/v1/analytics/overview`);
      if (response.ok) {
        const data = await response.json();
        setAnalyticsOverview(data);
      }
    } catch (err) {
      console.error("Failed to load analytics:", err);
    } finally {
      setAnalyticsLoading(false);
    }
  }

  useEffect(() => {
    if (!batchJobId) return;
    const interval = setInterval(async () => {
      try {
        const res = await fetch(`${apiBaseUrl}/api/v1/batch/status/${batchJobId}`);
        if (res.ok) {
          const data = await res.json();
          setBatchStatus(data);
          if (data.status === "COMPLETED" || data.status === "COMPLETED_WITH_ERRORS" || data.status === "FAILED") {
            setBatchLoading(false);
            clearInterval(interval);
            // Refresh library when batch is done
            if (activeTab === "library") fetchLibraryCandidates();
          }
        }
      } catch (e) {
        console.error(e);
      }
    }, 2000);
    return () => clearInterval(interval);
  }, [batchJobId, apiBaseUrl, activeTab]);

  async function fetchLibraryCandidates() {
    setLibraryLoading(true);
    try {
      const response = await fetch(`${apiBaseUrl}/api/v1/candidates`);
      if (response.ok) {
        const data = await response.json();
        setLibraryCandidates(data.items || []);
      }
    } catch (err) {
      console.error("Failed to load candidates library:", err);
    } finally {
      setLibraryLoading(false);
    }
  }

  function handleSelectLibraryCandidate(candidate: any) {
    setCandidateTwin(candidate as ApiCandidateTwin);
    
    // Add to candidate twins if not present
    setCandidateTwins(prev => {
      if (prev.some(t => t.candidate_id === candidate.candidate_id)) return prev;
      return [...prev, candidate as ApiCandidateTwin];
    });
    
    // Switch to workflow
    setActiveTab("workflow");
    
    // Reset subsequent steps
    setGraph(null);
    setEmbeddingCollection(null);
    setEvaluation(null);
    setRankings([]);
    setExplanation(null);
    setRecommendation(null);
    setCopilotDraft(null);
  }

  async function handleBatchUpload(e: React.ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0];
    if (!file) return;
    
    setBatchLoading(true);
    setError(null);
    try {
      const formData = new FormData();
      formData.append("file", file);
      
      const response = await fetch(`${apiBaseUrl}/api/v1/batch/upload-zip`, {
        method: "POST",
        body: formData,
      });
      if (!response.ok) throw new Error(`Batch upload failed with status ${response.status}`);
      const data = await response.json();
      setBatchJobId(data.job_id);
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "Unable to upload batch.");
      setBatchLoading(false);
    }
  }

      
      // Also fetch recommendation
      const recResponse = await fetch("/api/v1/recommend", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ role_id: roleDNA.role_id, candidate_id: candidateTwin.candidate_id }),
      });
      if (recResponse.ok) {
        const recPayload = (await recResponse.json()) as RecommendResponse;
        setRecommendation(recPayload.recommendation);
      }
      setCopilotDraft(null);
  async function handleCopilotDraft() {
    if (!roleDNA || !candidateTwin) return;
    setCopilotLoading(true);
    try {
      const response = await fetch("/api/v1/copilot/draft-email", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ role_id: roleDNA.role_id, candidate_id: candidateTwin.candidate_id }),
      });
      if (!response.ok) throw new Error(`Copilot failed with status ${response.status}`);
      const payload = (await response.json()) as CopilotResponse;
      setCopilotDraft(payload);
    } catch (caught) {
      console.error(caught);
    } finally {
      setCopilotLoading(false);
    }
  }

  async function handleCompare() {
    if (!candidateTwin || !compareCandidateId || !roleDNA) return;
    setComparisonLoading(true);
    setError(null);
    try {
      const response = await fetch(`${apiBaseUrl}/api/v1/compare`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          candidate_a_id: candidateTwin.candidate_id,
          candidate_b_id: compareCandidateId,
          role_id: roleDNA.role_id,
        })
      });
      if (!response.ok) throw new Error("Comparison failed");
      const data = await response.json();
      setComparisonMatrix(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to compare candidates.");
    } finally {
      setComparisonLoading(false);
    }
  }

          <button
            onClick={() => setActiveTab("analytics")}
            className={`border-b-2 py-2 px-1 text-sm font-medium ${activeTab === "analytics" ? "border-signal text-signal" : "border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700"}`}
          >
            Analytics
          </button>
      {activeTab === "workflow" && (
                className="h-10 rounded border border-gray-300 bg-white px-3 text-sm outline-none focus:border-signal focus:ring-2 focus:ring-blue-100 min-w-[200px]"
              >
                <option value="">Select Candidate to Compare</option>
                {libraryCandidates
                  .filter((c) => c.candidate_id !== candidateTwin?.candidate_id)
                  .map((c) => (
                    <option key={c.candidate_id} value={c.candidate_id}>
                      {c.name}
                    </option>
                  ))}
              </select>
              <button
                type="button"
                onClick={handleCompare}
                disabled={comparisonLoading || !candidateTwin || !compareCandidateId || !roleDNA}
                className="inline-flex h-10 items-center justify-center gap-2 rounded bg-signal px-4 text-sm font-semibold text-white disabled:cursor-not-allowed disabled:bg-gray-400"
              >
                {comparisonLoading ? <Loader2 className="h-4 w-4 animate-spin" aria-hidden="true" /> : <Layers3 className="h-4 w-4" aria-hidden="true" />}
                Compare
              </button>
            </div>
          {comparisonMatrix ? (
            <div className="space-y-6">
              <div className="rounded-lg bg-gray-50 border border-gray-200 p-5">
                <h4 className="font-semibold text-gray-900 mb-2">Comparison Summary</h4>
                <p className="text-sm text-gray-700 leading-relaxed mb-4">{comparisonMatrix.summary}</p>
                <h4 className="font-semibold text-gray-900 mb-2">Recommendation</h4>
                <p className="text-sm text-gray-700 leading-relaxed">{comparisonMatrix.recommendation}</p>
              <div className="overflow-x-auto border rounded border-gray-200">
                <table className="w-full text-left text-sm border-collapse whitespace-nowrap">
                  <thead>
                    <tr className="border-b border-gray-200 bg-gray-50">
                      <th className="py-3 px-4 font-semibold text-gray-600">Dimension</th>
                      <th className="py-3 px-4 font-semibold text-gray-900">{comparisonMatrix.candidate_a_name}</th>
                      <th className="py-3 px-4 font-semibold text-gray-900">{comparisonMatrix.candidate_b_name}</th>
                      <th className="py-3 px-4 font-semibold text-gray-600">Delta</th>
                    </tr>
                  </thead>
                  <tbody>
                    {comparisonMatrix.dimensions.map((dim, idx) => (
                      <tr key={idx} className="border-b border-gray-100 hover:bg-gray-50/50">
                        <td className="py-3 px-4 font-medium text-gray-700">{dim.dimension}</td>
                        <td className={`py-3 px-4 ${dim.winner === 'A' ? 'text-green-700 font-semibold bg-green-50/50' : 'text-gray-600'}`}>
                          {dim.candidate_a_score}
                        </td>
                        <td className={`py-3 px-4 ${dim.winner === 'B' ? 'text-green-700 font-semibold bg-green-50/50' : 'text-gray-600'}`}>
                          {dim.candidate_b_score}
                        </td>
                        <td className="py-3 px-4 text-gray-500">
                          {Math.abs(dim.delta) > 0 ? (dim.delta > 0 ? `+${dim.delta} (A)` : `+${Math.abs(dim.delta)} (B)`) : 'TIE'}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>

              <div className="grid md:grid-cols-3 gap-4">
                <div className="rounded border border-gray-200 bg-white p-4 shadow-sm">
                  <h4 className="text-sm font-semibold text-gray-800 mb-3">Shared Skills</h4>
                  <div className="flex flex-wrap gap-1.5">
                    {comparisonMatrix.skill_overlap.length > 0 ? comparisonMatrix.skill_overlap.map((s, i) => (
                      <span key={i} className="inline-block rounded-sm bg-gray-100 px-2 py-0.5 text-xs text-gray-600">{s}</span>
                    )) : <span className="text-xs text-gray-500">None detected</span>}
                  </div>
                </div>
                <div className="rounded border border-blue-100 bg-blue-50/30 p-4 shadow-sm">
                  <h4 className="text-sm font-semibold text-blue-800 mb-3">Unique to {comparisonMatrix.candidate_a_name}</h4>
                  <div className="flex flex-wrap gap-1.5">
                    {comparisonMatrix.a_unique_skills.length > 0 ? comparisonMatrix.a_unique_skills.map((s, i) => (
                      <span key={i} className="inline-block rounded-sm bg-blue-100 px-2 py-0.5 text-xs text-blue-700">{s}</span>
                    )) : <span className="text-xs text-gray-500">None detected</span>}
                  </div>
                </div>
                <div className="rounded border border-purple-100 bg-purple-50/30 p-4 shadow-sm">
                  <h4 className="text-sm font-semibold text-purple-800 mb-3">Unique to {comparisonMatrix.candidate_b_name}</h4>
                  <div className="flex flex-wrap gap-1.5">
                    {comparisonMatrix.b_unique_skills.length > 0 ? comparisonMatrix.b_unique_skills.map((s, i) => (
                      <span key={i} className="inline-block rounded-sm bg-purple-100 px-2 py-0.5 text-xs text-purple-700">{s}</span>
                    )) : <span className="text-xs text-gray-500">None detected</span>}
                  </div>
                </div>
            <EmptyState text="Select a second candidate from the library to generate a side-by-side comparison matrix." />

              {/* Recommendation Card */}
              {recommendation && (
                <div className="mt-4 p-4 rounded bg-emerald-50 border border-emerald-100 shadow-sm transition-all duration-300 text-ink">
                  <h4 className="text-sm font-semibold text-emerald-800 mb-3 flex items-center gap-2">
                    <Sparkles className="h-4 w-4 text-emerald-600" />
                    Final Recommendation
                  </h4>
                  <div className="flex flex-col md:flex-row gap-4 items-start">
                    <div className="shrink-0 px-3 py-1.5 rounded-full bg-emerald-600 text-white font-bold text-xs tracking-wide">
                      {recommendation.label.replace("_", " ")}
                    </div>
                    <div className="flex-1 space-y-2 text-sm text-graphite">
                      <p>{recommendation.reason}</p>
                      {recommendation.supporting_evidence.length > 0 && (
                        <ul className="list-disc list-inside pl-1 space-y-1 opacity-90 text-xs">
                          {recommendation.supporting_evidence.map((ev, i) => (
                            <li key={i}>{ev}</li>
                          ))}
                        </ul>
                      )}
                    </div>
                  </div>
                </div>
              )}

              {/* Copilot Card */}
              {recommendation && (
                <div className="mt-4 flex flex-col gap-3">
                  {!copilotDraft ? (
                    <button
                      type="button"
                      onClick={handleCopilotDraft}
                      disabled={copilotLoading}
                      className="inline-flex h-10 w-fit items-center justify-center gap-2 rounded bg-indigo-600 px-4 text-sm font-semibold text-white shadow hover:bg-indigo-700 disabled:cursor-not-allowed disabled:bg-gray-400"
                    >
                      {copilotLoading ? <Loader2 className="h-4 w-4 animate-spin" /> : <Sparkles className="h-4 w-4" />}
                      Draft Outreach Email
                    </button>
                  ) : (
                    <div className="p-4 rounded-xl border border-indigo-100 bg-indigo-50 shadow-sm transition-all duration-300">
                      <h4 className="text-sm font-semibold text-indigo-900 mb-3 flex items-center gap-2">
                        <Sparkles className="h-4 w-4 text-indigo-600" />
                        Copilot Drafted Email
                      </h4>
                      <div className="bg-white border border-indigo-100 rounded p-3 text-sm text-gray-800 space-y-2">
                        <p className="font-semibold border-b border-gray-100 pb-2 mb-2">Subject: {copilotDraft.subject}</p>
                        <pre className="whitespace-pre-wrap font-sans text-xs text-gray-700 leading-relaxed">
                          {copilotDraft.body}
                        </pre>
                      </div>
                    </div>
                  )}
                </div>
              )}
            <ExplanationPanel explanation={explanation} candidateName={candidateTwin?.name ?? explanation.candidate_id} ranking={currentRanking} />

        <ModulePanel
          eyebrow="AI Copilot"
          title="Recruiter Chat"
          icon={<Sparkles className="h-6 w-6 text-indigo-500" aria-hidden="true" />}
          form={null}
        >
          <CopilotChatPanel
            apiBaseUrl={apiBaseUrl}
            candidateId={candidateTwin?.candidate_id}
            roleId={roleDNA?.role_id}
          />
        </ModulePanel>
          <CandidateLibrary apiBaseUrl={apiBaseUrl} onSelectCandidate={handleSelectLibraryCandidate} />
type ExplanationSection = {
  title: string;
  items: string[];
  icon: string;
  bg: string;
  border: string;
  label_color: string;
  dot_color: string;
  fallback: string;
};

function ExplanationPanel({
  explanation,
  candidateName,
  ranking,
}: {
  explanation: ApiExplanationProfile;
  candidateName: string;
  ranking: ApiRankingResult;
}) {
  const sections: ExplanationSection[] = [
    {
      title: "Strengths",
      items: explanation.strengths,
      icon: "Γ£ª",
      bg: "bg-emerald-50",
      border: "border-emerald-200",
      label_color: "text-emerald-700",
      dot_color: "bg-emerald-500",
      fallback: "No major strength signal detected.",
    },
    {
      title: "Risks",
      items: explanation.risks,
      icon: "ΓÜá",
      bg: "bg-red-50",
      border: "border-red-200",
      label_color: "text-red-700",
      dot_color: "bg-red-500",
      fallback: "No major risk signal detected.",
    },
    {
      title: "Evidence",
      items: explanation.evidence ?? [],
      icon: "Γùë",
      bg: "bg-blue-50",
      border: "border-blue-200",
      label_color: "text-blue-700",
      dot_color: "bg-blue-500",
      fallback: "No resume evidence extracted.",
    },
    {
      title: "Estimations",
      items: explanation.estimations ?? [],
      icon: "ΓÅ▒",
      bg: "bg-amber-50",
      border: "border-amber-200",
      label_color: "text-amber-700",
      dot_color: "bg-amber-500",
      fallback: "No performance estimations generated.",
    },
  ];

  return (
    <div className="space-y-6">
      {/* Header stats */}
      <div className="grid gap-3 sm:grid-cols-3">
        <Summary label="Rank" value={`#${explanation.ranking_position}`} />
        <Summary label="Score" value={String(ranking.score)} />
        <Summary label="Candidate" value={candidateName} />
      </div>

      {/* 2├ù2 colour-coded sections */}
      <div className="grid gap-4 sm:grid-cols-2">
        {sections.map((sec) => (
          <div key={sec.title} className={`rounded-xl border ${sec.border} ${sec.bg} p-4`}>
            <h4 className={`mb-3 flex items-center gap-1.5 text-xs font-bold uppercase tracking-wider ${sec.label_color}`}>
              <span>{sec.icon}</span>
              {sec.title}
              <span className="ml-auto rounded-full bg-white px-1.5 py-0.5 text-[10px] font-semibold shadow-sm">
                {sec.items.length}
              </span>
            </h4>
            {sec.items.length > 0 ? (
              <ul className="space-y-2">
                {sec.items.map((item, i) => (
                  <li key={i} className="flex items-start gap-2 text-sm text-gray-700 leading-snug">
                    <span className={`mt-1.5 h-1.5 w-1.5 shrink-0 rounded-full ${sec.dot_color}`} />
                    {item}
                  </li>
                ))}
              </ul>
            ) : (
              <p className="text-xs italic text-gray-500">{sec.fallback}</p>
            )}
          </div>
        ))}
      </div>

      {/* Reasoning ΓÇö full-width */}
      {explanation.reasoning.length > 0 && (
        <div className="rounded-xl border border-indigo-200 bg-indigo-50 p-4">
          <h4 className="mb-3 flex items-center gap-1.5 text-xs font-bold uppercase tracking-wider text-indigo-700">
            <span>Γùå</span>
            Why This Candidate
            <span className="ml-auto rounded-full bg-white px-1.5 py-0.5 text-[10px] font-semibold shadow-sm">
              {explanation.reasoning.length}
            </span>
          </h4>
          <ol className="space-y-2">
            {explanation.reasoning.map((item, i) => (
              <li key={i} className="flex gap-2.5 text-sm text-gray-700 leading-snug">
                <span className="shrink-0 font-bold text-indigo-400 text-xs mt-0.5">{String(i + 1).padStart(2, "0")}</span>
                {item}
              </li>
            ))}
          </ol>
        </div>
      )}

      {/* Counterfactuals */}
      {explanation.counterfactuals.length > 0 && (
        <div className="rounded-xl border border-purple-200 bg-gradient-to-br from-purple-50 to-indigo-50 p-4">
          <h4 className="mb-3 text-xs font-bold uppercase tracking-wider text-purple-700">
            Γ£º How To Improve This Candidate&apos;s Fit
          </h4>
          <div className="grid gap-3 sm:grid-cols-2">
            {explanation.counterfactuals.map((item, i) => (
              <div key={i} className="rounded-lg border border-purple-100 bg-white p-3 text-sm text-gray-700 shadow-sm leading-snug">
                {item}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}


    <div className="grid gap-4 grid-cols-2 lg:grid-cols-5">
      {rows.map(([key, label]) => {
        const value = Number(source[key]) || 0;
        let colorClass = "bg-red-500";
        if (value >= 70) colorClass = "bg-green-500";
        else if (value >= 40) colorClass = "bg-yellow-500";

        return (
          <div key={String(key)} className="rounded border border-gray-100 bg-white p-3 shadow-sm hover:shadow transition-shadow">
            <h4 className="text-[10px] font-bold uppercase tracking-wider text-graphite mb-1">{label}</h4>
            <div className="flex items-end justify-between mb-2">
              <span className="text-xl font-bold text-ink">{value}</span>
              <span className="text-[10px] text-gray-400 font-medium mb-1">/100</span>
            </div>
            <div className="h-1.5 w-full rounded-full bg-gray-100 overflow-hidden">
              <div className={`h-full rounded-full ${colorClass}`} style={{ width: `${value}%` }} />
            </div>
          </div>
        );
      })}
function CopilotChatPanel({
  apiBaseUrl,
  candidateId,
  roleId,
}: {
  apiBaseUrl: string;
  candidateId?: string;
  roleId?: string;
}) {
  type ChatMessage = { role: "user" | "assistant"; content: string; intent?: string; followUps?: string[] };
  const [messages, setMessages] = useState<ChatMessage[]>([
    { role: "assistant", content: "Hi! I'm the TalentGraph Recruiter Copilot. Ask me about candidate strengths, risks, skills, growth, leadership, or hiring recommendations.", followUps: ["What are their strengths?", "What are the key risks?", "How do they match the role?"] }
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  async function sendMessage(text: string) {
    if (!text.trim()) return;
    const userMsg: ChatMessage = { role: "user", content: text };
    setMessages(prev => [...prev, userMsg]);
    setInput("");
    setLoading(true);
    try {
      const res = await fetch(`${apiBaseUrl}/api/v1/copilot/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: text, candidate_id: candidateId, role_id: roleId }),
      });
      if (res.ok) {
        const data = await res.json();
        setMessages(prev => [...prev, {
          role: "assistant",
          content: data.answer,
          intent: data.intent,
          followUps: data.follow_up_questions,
        }]);
      } else {
        setMessages(prev => [...prev, { role: "assistant", content: "Sorry, I couldn't process that request." }]);
      }
    } catch {
      setMessages(prev => [...prev, { role: "assistant", content: "Connection error. Please try again." }]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="flex flex-col gap-4">
      {/* Context badges */}
      <div className="flex gap-2 flex-wrap">
        {candidateId ? (
          <span className="rounded-full bg-blue-100 px-2.5 py-0.5 text-xs font-semibold text-blue-700">
            Candidate loaded
          </span>
        ) : (
          <span className="rounded-full bg-gray-100 px-2.5 py-0.5 text-xs text-gray-500">No candidate selected</span>
        )}
        {roleId ? (
          <span className="rounded-full bg-purple-100 px-2.5 py-0.5 text-xs font-semibold text-purple-700">
            Role loaded
          </span>
        ) : (
          <span className="rounded-full bg-gray-100 px-2.5 py-0.5 text-xs text-gray-500">No role selected</span>
        )}
      </div>

      {/* Chat window */}
      <div className="max-h-96 overflow-y-auto rounded-xl border border-gray-200 bg-gray-50 p-4 space-y-4">
        {messages.map((msg, i) => (
          <div key={i} className={`flex flex-col gap-1.5 ${msg.role === "user" ? "items-end" : "items-start"}`}>
            <div className={`max-w-[80%] rounded-2xl px-4 py-2.5 text-sm leading-snug ${
              msg.role === "user"
                ? "bg-signal text-white rounded-br-none"
                : "bg-white border border-gray-200 text-gray-800 rounded-bl-none shadow-sm"
            }`}>
              {msg.intent && msg.role === "assistant" && (
                <span className="mb-1 inline-block rounded-full bg-indigo-100 px-2 py-0.5 text-[10px] font-bold uppercase tracking-wider text-indigo-600">
                  {msg.intent}
                </span>
              )}
              <p>{msg.content}</p>
            </div>
            {msg.followUps && msg.followUps.length > 0 && (
              <div className="flex flex-wrap gap-1 mt-1">
                {msg.followUps.map((q, qi) => (
                  <button
                    key={qi}
                    onClick={() => sendMessage(q)}
                    className="rounded-full border border-indigo-200 bg-indigo-50 px-2.5 py-1 text-[11px] font-medium text-indigo-700 hover:bg-indigo-100 transition-colors"
                  >
                    {q}
                  </button>
                ))}
              </div>
            )}
          </div>
        ))}
        {loading && (
          <div className="flex items-start">
            <div className="rounded-2xl rounded-bl-none border border-gray-200 bg-white px-4 py-2.5 text-sm text-gray-400 shadow-sm">
              ThinkingΓÇª
            </div>
          </div>
        )}
        <div ref={bottomRef} />
      </div>

      {/* Input */}
      <form onSubmit={(e) => { e.preventDefault(); sendMessage(input); }} className="flex gap-2">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask about strengths, risks, skills, fitΓÇª"
          disabled={loading}
          className="flex-1 rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-signal focus:outline-none focus:ring-1 focus:ring-signal disabled:opacity-50"
        />
        <button
          type="submit"
          disabled={loading || !input.trim()}
          className="rounded-lg bg-signal px-4 py-2 text-sm font-semibold text-white hover:bg-signal/90 disabled:opacity-50"
        >
          Send
        </button>
      </form>
    </div>
  );
}

function SemanticSearchWidget() {
  const [query, setQuery] = useState("");
  const [matchType, setMatchType] = useState<"similar" | "transferable">("similar");
  const [results, setResults] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);

  async function handleSearch(e: React.FormEvent) {
    e.preventDefault();
    if (!query.trim()) return;
    setLoading(true);
    try {
      const apiBaseUrl = process.env.NEXT_PUBLIC_API_BASE_URL || "";
      const res = await fetch(`${apiBaseUrl}/api/v1/search/candidates?query=${encodeURIComponent(query)}&match_type=${matchType}&limit=5`);
      if (res.ok) {
        const data = await res.json();
        setResults(data);
      }
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="space-y-4">
      <form onSubmit={handleSearch} className="flex gap-2">
        <input
          type="text"
          placeholder="Search candidates by concept (e.g. distributed systems)..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          className="flex-1 rounded border border-gray-300 px-3 py-2 text-sm focus:border-signal focus:outline-none focus:ring-1 focus:ring-signal"
        />
        <select
          value={matchType}
          onChange={(e) => setMatchType(e.target.value as any)}
          className="rounded border border-gray-300 bg-white px-3 py-2 text-sm text-gray-700 focus:border-signal focus:outline-none"
        >
          <option value="similar">Direct Match</option>
          <option value="transferable">Transferable Talent</option>
        </select>
        <button
          type="submit"
          disabled={loading || !query.trim()}
          className="rounded bg-signal px-4 py-2 text-sm font-semibold text-white hover:bg-signal/90 disabled:opacity-50"
        >
          {loading ? "Searching..." : "Search"}
        </button>
      </form>
      
      {results.length > 0 && (
        <div className="space-y-2 mt-4">
          <h4 className="text-xs font-semibold text-gray-500 uppercase">Results</h4>
          {results.map((r, i) => (
            <div key={i} className="flex justify-between items-center bg-gray-50 p-2 rounded border border-gray-200">
              <div>
                <p className="text-sm font-semibold text-ink">{r.name}</p>
                <p className="text-xs text-gray-500">{r.source?.growth_stage}</p>
              </div>
              <div className="flex items-center gap-2">
                <span className={`text-xs font-bold ${r.score >= 0.75 ? 'text-green-600' : 'text-amber-600'}`}>
                  {(r.score * 100).toFixed(1)}% Match
                </span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

      {/* Semantic Search Panel */}
      <div className="rounded-xl border border-gray-200 bg-white p-4 shadow-sm">
        <p className="text-xs font-semibold uppercase tracking-wide text-graphite mb-3">
          Semantic Talent Search
        </p>
        <SemanticSearchWidget />
      </div>

