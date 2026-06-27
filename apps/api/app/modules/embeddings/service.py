from app.domain.candidate_twin import CandidateDigitalTwin
from app.domain.role_dna import RoleDNAProfile
from app.domain.vector import EmbeddingCollection, EmbeddingRecord, SummaryDocument
from app.modules.embeddings.summary_service import SummaryService
from app.providers.embedding_provider import EmbeddingProvider


class EmbeddingFoundationService:
    """Generates summaries and embeddings without similarity or ranking."""

    def __init__(self, summary_service: SummaryService, embedding_provider: EmbeddingProvider) -> None:
        self.summary_service = summary_service
        self.embedding_provider = embedding_provider

    def generate(
        self,
        role_dna: RoleDNAProfile | None = None,
        candidate_twin: CandidateDigitalTwin | None = None,
    ) -> EmbeddingCollection:
        summaries = self._summaries(role_dna, candidate_twin)
        embeddings: list[EmbeddingRecord] = []

        for summary, vector in zip(
            summaries,
            self.embedding_provider.embed_batch([summary.text for summary in summaries]),
            strict=True,
        ):
            embeddings.append(
                EmbeddingRecord(
                    id=f"embedding:{summary.id}",
                    source_id=summary.id,
                    kind=summary.kind,
                    text=summary.text,
                    vector=vector,
                    metadata=summary.metadata,
                )
            )

        for skill in self._skills(role_dna, candidate_twin):
            text = f"Skill: {skill}"
            embeddings.append(
                EmbeddingRecord(
                    id=f"embedding:skill:{self._slug(skill)}",
                    source_id=f"skill:{self._slug(skill)}",
                    kind="skill",
                    text=text,
                    vector=self.embedding_provider.embed(text),
                    metadata={"skill": skill},
                )
            )

        for project in candidate_twin.projects if candidate_twin is not None else []:
            text = f"Project: {project}"
            embeddings.append(
                EmbeddingRecord(
                    id=f"embedding:project:{self._slug(project)}",
                    source_id=f"project:{self._slug(project)}",
                    kind="project",
                    text=text,
                    vector=self.embedding_provider.embed(text),
                    metadata={"project": project},
                )
            )

        for domain in candidate_twin.domains if candidate_twin is not None else []:
            text = f"Domain: {domain}"
            embeddings.append(
                EmbeddingRecord(
                    id=f"embedding:domain:{self._slug(domain)}",
                    source_id=f"domain:{self._slug(domain)}",
                    kind="domain",
                    text=text,
                    vector=self.embedding_provider.embed(text),
                    metadata={"domain": domain},
                )
            )

        return EmbeddingCollection(
            collection_id=self._collection_id(role_dna, candidate_twin),
            summaries=summaries,
            embeddings=embeddings,
        )

    def _summaries(
        self,
        role_dna: RoleDNAProfile | None,
        candidate_twin: CandidateDigitalTwin | None,
    ) -> list[SummaryDocument]:
        summaries: list[SummaryDocument] = []
        if role_dna is not None:
            summaries.append(self.summary_service.role_summary(role_dna))
        if candidate_twin is not None:
            summaries.append(self.summary_service.candidate_summary(candidate_twin))
        if not summaries:
            raise ValueError("At least one role or candidate input is required to generate embeddings.")
        return summaries

    @staticmethod
    def _skills(role: RoleDNAProfile | None, candidate: CandidateDigitalTwin | None) -> list[str]:
        values: list[str] = []
        if role is not None:
            values.extend([*role.required_skills, *role.preferred_skills])
        if candidate is not None:
            values.extend(candidate.skills)
        return list(dict.fromkeys(values))

    @staticmethod
    def _collection_id(role: RoleDNAProfile | None, candidate: CandidateDigitalTwin | None) -> str:
        parts = ["embeddings"]
        if role is not None:
            parts.append(role.role_id)
        if candidate is not None:
            parts.append(candidate.candidate_id)
        return ":".join(parts)

    @staticmethod
    def _slug(value: str) -> str:
        return value.strip().casefold().replace(" ", "-").replace("/", "-")[:80]
