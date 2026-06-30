"use client";

import { useEffect, useState, useRef } from "react";
import { Loader2, Search, SlidersHorizontal, ChevronLeft, ChevronRight, User } from "lucide-react";
import { useVirtualizer } from '@tanstack/react-virtual';

type ApiCandidateTwin = {
  candidate_id: string;
  name: string;
  skills: string[];
  growth_stage: string;
  confidence: number;
};

type PaginatedCandidateListResponse = {
  items: ApiCandidateTwin[];
  total: number;
  page: number;
  page_size: number;
};

export default function CandidateLibrary({ 
  apiBaseUrl, 
  onSelectCandidate,
  onCandidatesLoaded 
}: { 
  apiBaseUrl: string;
  onSelectCandidate?: (candidate: ApiCandidateTwin) => void;
  onCandidatesLoaded?: (candidates: ApiCandidateTwin[]) => void;
}) {
  const [candidates, setCandidates] = useState<ApiCandidateTwin[]>([]);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(1);
  const [pageSize] = useState(500); // Increased for virtualization
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Filters
  const [search, setSearch] = useState("");
  const [semanticMode, setSemanticMode] = useState(false);
  const [growthStage, setGrowthStage] = useState("");
  const [minConfidence, setMinConfidence] = useState<number | "">("");

  const parentRef = useRef<HTMLDivElement>(null);

  const rowVirtualizer = useVirtualizer({
    count: candidates.length,
    getScrollElement: () => parentRef.current,
    estimateSize: () => 140, // estimated height of each candidate card in list view
    overscan: 5,
  });

  const fetchCandidates = async () => {
    setLoading(true);
    setError(null);
    try {
      if (semanticMode && search.trim() !== "") {
        const res = await fetch(`${apiBaseUrl}/api/v1/search/candidates?query=${encodeURIComponent(search)}&limit=${pageSize}`);
        if (!res.ok) throw new Error("Failed to search candidates semantically");
        const data = (await res.json()) as any[];
        // Map the SearchResult structure back to CandidateTwin format
        setCandidates(data.map(d => d.source));
        setTotal(data.length);
      } else {
        const params = new URLSearchParams({
          page: page.toString(),
          page_size: pageSize.toString(),
        });
        if (search) params.append("search", search);
        if (growthStage) params.append("growth_stage", growthStage);
        if (minConfidence !== "") params.append("min_confidence", minConfidence.toString());

        const res = await fetch(`${apiBaseUrl}/api/v1/candidates?${params.toString()}`);
        if (!res.ok) throw new Error("Failed to fetch candidates");
        const data = (await res.json()) as PaginatedCandidateListResponse;
        setCandidates(data.items);
        setTotal(data.total);
        if (onCandidatesLoaded) {
          onCandidatesLoaded(data.items);
        }
      }
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchCandidates();
  }, [page, search, growthStage, minConfidence, semanticMode]);

  const totalPages = Math.ceil(total / pageSize) || 1;

  return (
    <div className="flex flex-col md:flex-row gap-6 mt-6">
      {/* Sidebar Filters */}
      <div className="w-full md:w-64 shrink-0 space-y-6 rounded border border-gray-200 dark:border-slate-800 bg-white dark:bg-slate-900 p-5 shadow-sm h-fit">
        <div className="flex items-center gap-2 border-b border-gray-100 pb-4">
          <SlidersHorizontal className="h-5 w-5 text-graphite dark:text-slate-400" />
          <h3 className="font-semibold text-ink dark:text-slate-50">Filters</h3>
        </div>

        <div className="space-y-4">
          <div>
            <label className="text-sm font-medium text-graphite dark:text-slate-400 block mb-1">Search</label>
            <div className="relative">
              <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-gray-400" />
              <input
                type="text"
                placeholder="Name or role..."
                value={search}
                onChange={(e) => { setSearch(e.target.value); setPage(1); }}
                className="w-full rounded border border-gray-300 dark:border-slate-700 py-2 pl-9 pr-3 text-sm focus:border-signal focus:outline-none focus:ring-1 focus:ring-signal"
              />
            </div>
            <div className="mt-2 flex items-center gap-2">
              <input
                type="checkbox"
                id="semantic-mode"
                checked={semanticMode}
                onChange={(e) => { setSemanticMode(e.target.checked); setPage(1); }}
                className="rounded border-gray-300 dark:border-slate-700 text-signal focus:ring-signal"
              />
              <label htmlFor="semantic-mode" className="text-xs font-medium text-graphite dark:text-slate-400">
                Semantic Search
              </label>
            </div>
          </div>

          <div>
            <label className="text-sm font-medium text-graphite dark:text-slate-400 block mb-1">Growth Stage</label>
            <select
              value={growthStage}
              onChange={(e) => { setGrowthStage(e.target.value); setPage(1); }}
              className="w-full rounded border border-gray-300 dark:border-slate-700 p-2 text-sm focus:border-signal focus:outline-none"
            >
              <option value="">All Stages</option>
              <option value="Explorer">Explorer</option>
              <option value="Builder">Builder</option>
              <option value="Operator">Operator</option>
              <option value="Scaler">Scaler</option>
              <option value="Leader">Leader</option>
            </select>
          </div>

          <div>
            <label className="text-sm font-medium text-graphite dark:text-slate-400 block mb-1">Min Confidence (%)</label>
            <input
              type="number"
              min="0"
              max="100"
              value={minConfidence}
              onChange={(e) => { setMinConfidence(e.target.value ? Number(e.target.value) : ""); setPage(1); }}
              className="w-full rounded border border-gray-300 dark:border-slate-700 p-2 text-sm focus:border-signal focus:outline-none focus:ring-1 focus:ring-signal"
            />
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 space-y-4">
        <div className="flex items-center justify-between">
          <h2 className="text-xl font-semibold text-ink dark:text-slate-50">Candidates ({total})</h2>
        </div>

        {error && <div className="rounded border border-red-200 bg-red-50 p-3 text-sm text-red-700">{error}</div>}

        {loading ? (
          <div className="flex justify-center p-10"><Loader2 className="h-8 w-8 animate-spin text-gray-400" /></div>
        ) : candidates.length === 0 ? (
          <div className="rounded border border-dashed border-gray-300 dark:border-slate-700 p-10 text-center text-graphite dark:text-slate-400">
            No candidates found matching the filters.
          </div>
        ) : (
          <div ref={parentRef} className="h-[600px] overflow-auto border border-gray-200 dark:border-slate-800 rounded bg-gray-50 dark:bg-slate-900/50 p-2">
            <div
              style={{
                height: `${rowVirtualizer.getTotalSize()}px`,
                width: '100%',
                position: 'relative',
              }}
            >
              {rowVirtualizer.getVirtualItems().map((virtualRow) => {
                const c = candidates[virtualRow.index];
                if (!c) return null;
                return (
                  <div
                    key={virtualRow.index}
                    style={{
                      position: 'absolute',
                      top: 0,
                      left: 0,
                      width: '100%',
                      height: `${virtualRow.size}px`,
                      transform: `translateY(${virtualRow.start}px)`,
                      paddingBottom: '8px' // Gap simulation
                    }}
                  >
                    <div 
                      className={`h-full rounded border border-gray-200 dark:border-slate-800 bg-white dark:bg-slate-900 p-4 shadow-sm transition-shadow ${onSelectCandidate ? 'cursor-pointer hover:shadow-md hover:border-signal/50' : 'hover:shadow'}`}
                      onClick={() => onSelectCandidate?.(c)}
                    >
                <div className="flex items-center gap-3">
                  <div className="flex h-10 w-10 items-center justify-center rounded-full bg-blue-50 text-signal">
                    <User className="h-5 w-5" />
                  </div>
                  <div>
                    <h3 className="font-semibold text-ink dark:text-slate-50">{c.name}</h3>
                    <p className="text-xs text-graphite dark:text-slate-400 font-medium">{c.growth_stage}</p>
                  </div>
                </div>
                
                <div className="mt-4 pt-4 border-t border-gray-100">
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-xs text-graphite dark:text-slate-400">Confidence</span>
                    <span className="text-xs font-semibold text-signal">{c.confidence}%</span>
                  </div>
                  <div className="flex flex-wrap gap-1.5 mt-2">
                    {c.skills.slice(0, 5).map((s) => (
                      <span key={s} className="rounded bg-gray-100 dark:bg-slate-800 px-2 py-0.5 text-[10px] font-medium text-gray-600 dark:text-slate-400">
                        {s}
                      </span>
                    ))}
                    {c.skills.length > 5 && (
                      <span className="rounded bg-gray-50 dark:bg-slate-800/50 px-2 py-0.5 text-[10px] font-medium text-gray-500 dark:text-slate-400">
                        +{c.skills.length - 5}
                      </span>
                    )}
                  </div>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  )}

        {/* Pagination */}
        {total > 0 && (
          <div className="flex items-center justify-between border-t border-gray-200 dark:border-slate-800 bg-white dark:bg-slate-900 px-4 py-3 sm:px-6 rounded shadow-sm">
            <div className="hidden sm:flex sm:flex-1 sm:items-center sm:justify-between">
              <div>
                <p className="text-sm text-gray-700 dark:text-slate-300">
                  Showing <span className="font-medium">{(page - 1) * pageSize + 1}</span> to{" "}
                  <span className="font-medium">{Math.min(page * pageSize, total)}</span> of{" "}
                  <span className="font-medium">{total}</span> results
                </p>
              </div>
              <div>
                <nav className="isolate inline-flex -space-x-px rounded-md shadow-sm" aria-label="Pagination">
                  <button
                    onClick={() => setPage(p => Math.max(1, p - 1))}
                    disabled={page === 1}
                    className="relative inline-flex items-center rounded-l-md px-2 py-2 text-gray-400 ring-1 ring-inset ring-gray-300 hover:bg-gray-50 dark:bg-slate-800/50 focus:z-20 focus:outline-offset-0 disabled:opacity-50"
                  >
                    <span className="sr-only">Previous</span>
                    <ChevronLeft className="h-5 w-5" aria-hidden="true" />
                  </button>
                  <span className="relative inline-flex items-center px-4 py-2 text-sm font-semibold text-gray-700 dark:text-slate-300 ring-1 ring-inset ring-gray-300">
                    {page} / {totalPages}
                  </span>
                  <button
                    onClick={() => setPage(p => Math.min(totalPages, p + 1))}
                    disabled={page === totalPages}
                    className="relative inline-flex items-center rounded-r-md px-2 py-2 text-gray-400 ring-1 ring-inset ring-gray-300 hover:bg-gray-50 dark:bg-slate-800/50 focus:z-20 focus:outline-offset-0 disabled:opacity-50"
                  >
                    <span className="sr-only">Next</span>
                    <ChevronRight className="h-5 w-5" aria-hidden="true" />
                  </button>
                </nav>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
