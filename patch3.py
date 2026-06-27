with open('patched2.tsx', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
for i, line in enumerate(lines):
    # Fix the activeTab rendering
    if line.strip() == '{activeTab === "workflow" ? (':
        new_lines.append('      {activeTab === "workflow" && (\n')
        continue
    if line.strip() == ') : (':
        new_lines.append('      )}\n\n      {activeTab === "library" && (\n')
        continue

    # Add the function implementations before return (
    if line.strip() == 'return (':
        if 'handleCopilotDraft' not in ''.join(new_lines[-20:]):
            new_lines.append('''
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

''')
        new_lines.append(line)
        continue

    # Insert Copilot in Explainable Reasoning
    if line.strip() == 'Explain Best Match':
        new_lines.append(line)
        new_lines.append('''                  </button>
                  <button
                    type="button"
                    onClick={handleCopilotDraft}
                    disabled={copilotLoading || !candidateTwin}
                    className="inline-flex h-10 items-center justify-center gap-2 rounded border border-gray-300 bg-white px-4 text-sm font-semibold text-ink disabled:cursor-not-allowed disabled:text-gray-400"
                  >
                    {copilotLoading ? <Loader2 className="h-4 w-4 animate-spin" aria-hidden="true" /> : <Send className="h-4 w-4" aria-hidden="true" />}
                    Draft Outreach''')
        continue

    # Insert Copilot Draft View
    if line.strip() == '{explanation ? (':
        new_lines.append('''              {copilotDraft && (
                <div className="mb-6 rounded-lg border border-gray-200 bg-white shadow-sm overflow-hidden animate-fade-in">
                  <div className="bg-gray-50 px-4 py-3 border-b border-gray-200 flex justify-between items-center">
                    <span className="text-xs font-bold uppercase text-gray-500 flex items-center gap-2">
                      <Send className="h-3 w-3" /> Outreach Draft
                    </span>
                  </div>
                  <div className="p-4 space-y-3">
                    <div>
                      <span className="text-xs font-semibold text-gray-400 uppercase">Subject</span>
                      <p className="text-sm font-medium text-gray-900">{copilotDraft.subject}</p>
                    </div>
                    <div>
                      <span className="text-xs font-semibold text-gray-400 uppercase">Body</span>
                      <div className="mt-1 p-3 bg-gray-50 rounded text-sm text-gray-800 whitespace-pre-wrap border border-gray-100">
                        {copilotDraft.body}
                      </div>
                    </div>
                  </div>
                </div>
              )}

''')
        new_lines.append(line)
        continue

    # Insert Copilot Chat Panel
    if line.strip() == 'Generate semantic embeddings to inspect role and candidate concept overlap.':
        new_lines.append(line)
        continue
    
    if line.strip() == '</ModulePanel>' and lines[i-3].strip() == 'Generate semantic embeddings to inspect role and candidate concept overlap." />':
        new_lines.append(line)
        new_lines.append('''
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
''')
        continue

    # Insert Recommendation in Evaluate
    if line.strip() == '<EvaluatorCard title="Culture" result={evaluation.culture} />':
        new_lines.append(line)
        continue
    
    if line.strip() == '</div>' and lines[i-1].strip() == '<EvaluatorCard title="Culture" result={evaluation.culture} />':
        new_lines.append(line)
        new_lines.append('''
                  {/* Recommendation Card */}
                  {recommendation && (
                    <div className="mt-4 p-4 rounded bg-emerald-50 border border-emerald-100 shadow-sm transition-all duration-300 text-ink">
                      <h4 className="text-sm font-semibold text-emerald-800 mb-3 flex items-center gap-2">
                        <Sparkles className="h-4 w-4 text-emerald-600" />
                        Final Recommendation
                      </h4>
                      <div className="flex items-start gap-4">
                        <div className="shrink-0 flex flex-col items-center justify-center h-16 w-16 rounded-full bg-white border-4 border-emerald-200 shadow-inner">
                          <span className="text-[10px] uppercase font-bold text-gray-500 mb-0.5">Decision</span>
                          <span className="text-sm font-extrabold text-emerald-600">{recommendation.label === 'STRONG_HIRE' ? 'A+' : recommendation.label === 'HIRE' ? 'A' : recommendation.label === 'GROWTH_HIRE' ? 'B' : recommendation.label === 'BORDERLINE' ? 'C' : 'D'}</span>
                        </div>
                        <div>
                          <p className="text-sm text-gray-800 font-medium">{recommendation.reason}</p>
                          <ul className="mt-2 space-y-1">
                            {recommendation.supporting_evidence.map((ev, i) => (
                              <li key={i} className="text-xs text-emerald-700 flex items-start gap-1.5">
                                <span className="text-emerald-500 mt-0.5">•</span> {ev}
                              </li>
                            ))}
                          </ul>
                        </div>
                      </div>
                    </div>
                  )}
''')
        continue

    # Insert Comparison Matrix in Step 2
    if line.strip() == 'Build a Candidate Digital Twin to inspect skills, timeline, growth stage, and reasoning.':
        new_lines.append(line)
        continue
        
    if line.strip() == '</ModulePanel>' and lines[i-2].strip() == 'Build a Candidate Digital Twin to inspect skills, timeline, growth stage, and reasoning." />':
        new_lines.append(line)
        new_lines.append('''      </section>

      <section className="mx-auto max-w-7xl px-6 pb-8">
        <ModulePanel
          eyebrow="Workspace"
          title="Candidate Comparison"
          icon={<UserRound className="h-6 w-6 text-purple-600" aria-hidden="true" />}
          form={
            <div className="flex flex-wrap items-center gap-3">
              <select
                value={compareCandidateId}
                onChange={(e) => setCompareCandidateId(e.target.value)}
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
          }
        >
          {comparisonMatrix ? (
            <div className="space-y-6">
              <div className="rounded-lg bg-gray-50 border border-gray-200 p-5">
                <h4 className="font-semibold text-gray-900 mb-2">Comparison Summary</h4>
                <p className="text-sm text-gray-700 leading-relaxed mb-4">{comparisonMatrix.summary}</p>
                <h4 className="font-semibold text-gray-900 mb-2">Recommendation</h4>
                <p className="text-sm text-gray-700 leading-relaxed">{comparisonMatrix.recommendation}</p>
              </div>

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
              </div>
            </div>
          ) : (
            <EmptyState text="Select a second candidate from the library to generate a side-by-side comparison matrix." />
          )}
        </ModulePanel>
''')
        continue

    # Insert Analytics section at the end
    if line.strip() == '<CandidateLibrary apiBaseUrl={apiBaseUrl} onSelectCandidate={handleSelectLibraryCandidate} />':
        new_lines.append(line)
        continue
    
    if line.strip() == '</section>' and lines[i-1].strip() == '<CandidateLibrary apiBaseUrl={apiBaseUrl} onSelectCandidate={handleSelectLibraryCandidate} />':
        new_lines.append(line)
        new_lines.append('''      )}

      {activeTab === "analytics" && (
        <section className="mx-auto max-w-7xl px-6 pb-8">
          {analyticsLoading ? (
            <div className="flex items-center justify-center py-20 text-graphite gap-2">
              <Loader2 className="h-5 w-5 animate-spin" />
              Loading analytics...
            </div>
          ) : analyticsOverview ? (
            <div className="space-y-6 animate-fade-in">
              <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mt-6">
                <div className="rounded-xl border border-gray-200 bg-white p-5 shadow-sm">
                  <p className="text-sm font-semibold text-gray-500">Total Candidates</p>
                  <p className="mt-2 text-3xl font-bold text-gray-900">{analyticsOverview.total_candidates}</p>
                </div>
                <div className="rounded-xl border border-gray-200 bg-white p-5 shadow-sm">
                  <p className="text-sm font-semibold text-gray-500">Total Roles</p>
                  <p className="mt-2 text-3xl font-bold text-gray-900">{analyticsOverview.total_roles}</p>
                </div>
                <div className="rounded-xl border border-gray-200 bg-white p-5 shadow-sm">
                  <p className="text-sm font-semibold text-gray-500">Evaluations Run</p>
                  <p className="mt-2 text-3xl font-bold text-gray-900">{analyticsOverview.total_evaluations}</p>
                </div>
                <div className="rounded-xl border border-gray-200 bg-white p-5 shadow-sm">
                  <p className="text-sm font-semibold text-gray-500">Avg Confidence</p>
                  <p className="mt-2 text-3xl font-bold text-gray-900">{analyticsOverview.average_confidence}%</p>
                </div>
              </div>

              <div className="grid lg:grid-cols-2 gap-6">
                <div className="rounded border border-gray-200 bg-white p-6 shadow-sm">
                  <h3 className="font-semibold text-gray-800 mb-4 flex items-center gap-2">
                    <BarChart3 className="h-5 w-5 text-signal" />
                    Growth Stage Distribution
                  </h3>
                  <div className="space-y-4">
                    {analyticsOverview.growth_stage_distribution.length > 0 ? (
                      analyticsOverview.growth_stage_distribution.map((dist, idx) => (
                        <div key={idx} className="flex items-center gap-3">
                          <span className="w-24 shrink-0 text-sm font-medium text-gray-700 truncate">{dist.growth_stage}</span>
                          <div className="flex-1 h-2.5 rounded bg-gray-100">
                            <div className="h-2.5 rounded bg-signal" style={{ width: `${(dist.count / Math.max(1, analyticsOverview.total_candidates)) * 100}%` }} />
                          </div>
                          <span className="w-8 text-right text-xs text-gray-500 font-semibold">{dist.count}</span>
                        </div>
                      ))
                    ) : (
                      <p className="text-sm text-gray-500">No data available.</p>
                    )}
                  </div>
                </div>

                <div className="rounded border border-gray-200 bg-white p-6 shadow-sm">
                  <h3 className="font-semibold text-gray-800 mb-4 flex items-center gap-2">
                    <Brain className="h-5 w-5 text-mint" />
                    Top Required Skills
                  </h3>
                  <div className="flex flex-wrap gap-2">
                    {analyticsOverview.top_skills.length > 0 ? (
                      analyticsOverview.top_skills.map((skill, idx) => (
                        <div key={idx} className="inline-flex items-center gap-1.5 rounded-full border border-gray-200 bg-gray-50 px-3 py-1 text-sm font-medium text-gray-700">
                          {skill.skill}
                          <span className="rounded-full bg-gray-200 px-1.5 py-0.5 text-[10px] font-bold text-gray-600">{skill.count}</span>
                        </div>
                      ))
                    ) : (
                      <p className="text-sm text-gray-500">No skills extracted yet.</p>
                    )}
                  </div>
                </div>
              </div>
            </div>
          ) : (
            <EmptyState text="Run candidates through the pipeline to generate analytics data." />
          )}
        </section>
''')
        continue

    new_lines.append(line)

with open('patched3.tsx', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)
print('Patched UI sections!')
