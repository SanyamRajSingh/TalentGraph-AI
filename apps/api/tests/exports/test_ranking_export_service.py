from io import BytesIO

from openpyxl import load_workbook

from app.domain.candidate_twin import CandidateDigitalTwin
from app.domain.explanation import ExplanationProfile
from app.domain.ranking import HiringPersona, RankingResult
from app.modules.exports import RankingExportService
from app.repositories.memory import (
    InMemoryCandidateRepository,
    InMemoryExplanationRepository,
    InMemoryRankingRepository,
)


def test_ranking_export_service_generates_xlsx_rows() -> None:
    candidate_repository = InMemoryCandidateRepository()
    ranking_repository = InMemoryRankingRepository()
    explanation_repository = InMemoryExplanationRepository()
    candidate_repository.save(CandidateDigitalTwin(candidate_id="candidate_export", name="Ada Export"))
    ranking_repository.save_many(
        [
            RankingResult(
                candidate_id="candidate_export",
                role_id="role_export",
                rank=1,
                persona=HiringPersona.STARTUP_FOUNDER,
                score=88,
                confidence=81,
                evaluation_id="evaluation_export",
            )
        ]
    )
    explanation_repository.save(
        ExplanationProfile(
            candidate_id="candidate_export",
            role_id="role_export",
            ranking_position=1,
            strengths=["Strong Python alignment."],
            risks=["Limited fintech evidence."],
        )
    )

    content = RankingExportService(
        ranking_repository=ranking_repository,
        candidate_repository=candidate_repository,
        explanation_repository=explanation_repository,
    ).export_rankings(role_id="role_export", persona="startup_founder")

    workbook = load_workbook(BytesIO(content))
    sheet = workbook["Rankings"]
    assert [sheet.cell(row=1, column=column).value for column in range(1, 7)] == [
        "Rank",
        "Candidate Name",
        "Score",
        "Confidence",
        "Strengths",
        "Risks",
    ]
    assert sheet["A2"].value == 1
    assert sheet["B2"].value == "Ada Export"
    assert sheet["C2"].value == 88
    assert sheet["E2"].value == "Strong Python alignment."
    assert sheet["F2"].value == "Limited fintech evidence."
