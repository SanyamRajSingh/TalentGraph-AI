import math
from typing import Protocol

from pydantic import BaseModel

from app.domain.candidate_twin import CandidateDigitalTwin
from app.domain.role_dna import RoleDNAProfile
from app.repositories.candidate_repository import CandidateFilter


class EmbeddingProviderProtocol(Protocol):
    def embed(self, text: str) -> list[float]:
        ...
    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        ...


class SearchResult(BaseModel):
    id: str
    name: str
    score: float
    type: str  # "candidate" or "role"
    source: CandidateDigitalTwin | RoleDNAProfile


def cosine_similarity(v1: list[float], v2: list[float]) -> float:
    dot_product = sum(a * b for a, b in zip(v1, v2))
    norm_a = math.sqrt(sum(a * a for a in v1))
    norm_b = math.sqrt(sum(b * b for b in v2))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot_product / (norm_a * norm_b)


class SearchService:
    """Service for semantic search over candidates and roles."""

    def __init__(
        self,
        candidate_repository,
        role_repository,
        embedding_provider: EmbeddingProviderProtocol,
    ) -> None:
        self.candidate_repository = candidate_repository
        self.role_repository = role_repository
        self.embedding_provider = embedding_provider
        # Simple in-memory cache for vectors to speed up repeated searches
        self._vector_cache: dict[str, list[float]] = {}

    def _get_candidate_text(self, candidate: CandidateDigitalTwin) -> str:
        skills = ", ".join(candidate.skills)
        return f"{candidate.name}. Growth stage: {candidate.growth_stage}. Skills: {skills}."

    def _get_role_text(self, role: RoleDNAProfile) -> str:
        req = ", ".join(role.required_skills)
        pref = ", ".join(role.preferred_skills)
        return f"{role.role_title}. Archetype: {role.role_archetype}. Required: {req}. Preferred: {pref}."

    def _get_candidate_vector(self, candidate: CandidateDigitalTwin) -> list[float]:
        if candidate.candidate_id not in self._vector_cache:
            text = self._get_candidate_text(candidate)
            self._vector_cache[candidate.candidate_id] = self.embedding_provider.embed(text)
        return self._vector_cache[candidate.candidate_id]

    def _get_role_vector(self, role: RoleDNAProfile) -> list[float]:
        if role.role_id not in self._vector_cache:
            text = self._get_role_text(role)
            self._vector_cache[role.role_id] = self.embedding_provider.embed(text)
        return self._vector_cache[role.role_id]

    def find_candidates(self, query: str, limit: int = 10) -> list[SearchResult]:
        query_vector = self.embedding_provider.embed(query)
        # We need to fetch all candidates to search them (since we don't have a vector db yet)
        candidates = self.candidate_repository.search_candidates(CandidateFilter(page_size=1000)).items
        results = []
        for candidate in candidates:
            vec = self._get_candidate_vector(candidate)
            score = cosine_similarity(query_vector, vec)
            results.append(SearchResult(id=candidate.candidate_id, name=candidate.name, score=score, type="candidate", source=candidate))
        results.sort(key=lambda x: x.score, reverse=True)
        return results[:limit]

    def find_similar_candidates(self, candidate_id: str, limit: int = 10, match_type: str = "similar") -> list[SearchResult]:
        source = self.candidate_repository.get_by_candidate_id(candidate_id)
        if not source:
            raise ValueError("Candidate not found")
        query_vector = self._get_candidate_vector(source)
        
        candidates = self.candidate_repository.search_candidates(CandidateFilter(page_size=1000)).items
        results = []
        for candidate in candidates:
            if candidate.candidate_id == candidate_id:
                continue
            vec = self._get_candidate_vector(candidate)
            score = cosine_similarity(query_vector, vec)
            
            # Filter based on match_type
            if match_type == "similar" and score < 0.75:
                continue
            elif match_type == "transferable" and (score >= 0.75 or score < 0.40):
                continue
                
            results.append(SearchResult(id=candidate.candidate_id, name=candidate.name, score=score, type="candidate", source=candidate))
        
        results.sort(key=lambda x: x.score, reverse=True)
        return results[:limit]

    def find_candidates_for_role(self, role_id: str, limit: int = 10) -> list[SearchResult]:
        role = self.role_repository.get_by_role_id(role_id)
        if not role:
            raise ValueError("Role not found")
        query_vector = self._get_role_vector(role)

        candidates = self.candidate_repository.search_candidates(CandidateFilter(page_size=1000)).items
        results = []
        for candidate in candidates:
            vec = self._get_candidate_vector(candidate)
            score = cosine_similarity(query_vector, vec)
            results.append(SearchResult(id=candidate.candidate_id, name=candidate.name, score=score, type="candidate", source=candidate))
        results.sort(key=lambda x: x.score, reverse=True)
        return results[:limit]

    def find_roles(self, query: str, limit: int = 10) -> list[SearchResult]:
        query_vector = self.embedding_provider.embed(query)
        roles = self.role_repository.list_role_dna()
        results = []
        for role in roles:
            vec = self._get_role_vector(role)
            score = cosine_similarity(query_vector, vec)
            results.append(SearchResult(id=role.role_id, name=role.role_title, score=score, type="role", source=role))
        results.sort(key=lambda x: x.score, reverse=True)
        return results[:limit]

    def find_similar_roles(self, role_id: str, limit: int = 10) -> list[SearchResult]:
        source = self.role_repository.get_by_role_id(role_id)
        if not source:
            raise ValueError("Role not found")
        query_vector = self._get_role_vector(source)
        
        roles = self.role_repository.list_role_dna()
        results = []
        for role in roles:
            if role.role_id == role_id:
                continue
            vec = self._get_role_vector(role)
            score = cosine_similarity(query_vector, vec)
            results.append(SearchResult(id=role.role_id, name=role.role_title, score=score, type="role", source=role))
        results.sort(key=lambda x: x.score, reverse=True)
        return results[:limit]
