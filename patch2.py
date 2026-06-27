with open('patched1.tsx', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
skip_active_tab = False
for i, line in enumerate(lines):
    if line.strip() == 'const [activeTab, setActiveTab] = useState<"workflow" | "library">("workflow");':
        new_lines.append('  const [activeTab, setActiveTab] = useState<"workflow" | "library" | "analytics">("workflow");\n')
        continue

    if line.strip() == 'const [libraryLoading, setLibraryLoading] = useState(false);':
        new_lines.append(line)
        new_lines.append('''  const [recommendation, setRecommendation] = useState<ApiRecommendationResult | null>(null);
  const [copilotDraft, setCopilotDraft] = useState<ApiCopilotDraftResult | null>(null);
  const [copilotLoading, setCopilotLoading] = useState(false);
  const [analyticsOverview, setAnalyticsOverview] = useState<ApiAnalyticsOverview | null>(null);
  const [analyticsLoading, setAnalyticsLoading] = useState(false);
  const [compareCandidateId, setCompareCandidateId] = useState<string>("");
  const [comparisonMatrix, setComparisonMatrix] = useState<ApiComparisonMatrix | null>(null);
  const [comparisonLoading, setComparisonLoading] = useState(false);
''')
        continue

    if line.strip() == 'if (activeTab === "library") {':
        new_lines.append('    if (activeTab === "library") {\n')
        continue
        
    if line.strip() == 'fetchLibraryCandidates();':
        new_lines.append(line)
        new_lines.append('    } else if (activeTab === "analytics") {\n')
        new_lines.append('      fetchAnalyticsData();\n')
        continue

    if line.strip() == '}, [activeTab]);':
        new_lines.append(line)
        new_lines.append('''

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
''')
        continue

    if line.strip() == 'setActiveTab("workflow");':
        new_lines.append(line)
        new_lines.append('''    setRecommendation(null);
    setCopilotDraft(null);
    setComparisonMatrix(null);
''')
        continue

    if line.strip() == 'onClick={() => setActiveTab("library")}':
        new_lines.append(line)
        continue

    if line.strip() == 'Candidate Library':
        new_lines.append(line)
        new_lines.append('''          </button>
          <button
            onClick={() => setActiveTab("analytics")}
            className={`border-b-2 py-2 px-1 text-sm font-medium ${activeTab === "analytics" ? "border-signal text-signal" : "border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700"}`}
          >
            Analytics''')
        continue

    new_lines.append(line)

with open('patched2.tsx', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)
print('Patched state variables!')
