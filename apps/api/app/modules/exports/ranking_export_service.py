from copy import copy
from io import BytesIO

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill
from openpyxl.worksheet.worksheet import Worksheet

from app.repositories.candidate_repository import CandidateRepository
from app.repositories.explanation_repository import ExplanationRepository
from app.repositories.ranking_repository import RankingRepository


class RankingExportService:
    """Builds XLSX exports from existing ranking and explanation data."""

    HEADERS = ["Rank", "Candidate Name", "Score", "Confidence", "Strengths", "Risks"]

    def __init__(
        self,
        ranking_repository: RankingRepository,
        candidate_repository: CandidateRepository,
        explanation_repository: ExplanationRepository,
    ) -> None:
        self.ranking_repository = ranking_repository
        self.candidate_repository = candidate_repository
        self.explanation_repository = explanation_repository

    def export_rankings(self, role_id: str, persona: str | None = None) -> bytes:
        rankings = self.ranking_repository.list_by_role_id(role_id, persona=persona)
        workbook = Workbook()
        sheet = workbook.active
        sheet.title = "Rankings"
        self._write_header(sheet)

        for row_index, ranking in enumerate(rankings, start=2):
            candidate = self.candidate_repository.get_by_candidate_id(ranking.candidate_id)
            explanation = self.explanation_repository.get_by_candidate_id(ranking.candidate_id)
            sheet.cell(row=row_index, column=1, value=ranking.rank)
            sheet.cell(row=row_index, column=2, value=candidate.name if candidate else ranking.candidate_id)
            sheet.cell(row=row_index, column=3, value=ranking.score)
            sheet.cell(row=row_index, column=4, value=ranking.confidence)
            sheet.cell(row=row_index, column=5, value="\n".join(explanation.strengths) if explanation else "")
            sheet.cell(row=row_index, column=6, value="\n".join(explanation.risks) if explanation else "")

        self._format(sheet)
        buffer = BytesIO()
        workbook.save(buffer)
        return buffer.getvalue()

    def _write_header(self, sheet: Worksheet) -> None:
        for column_index, header in enumerate(self.HEADERS, start=1):
            cell = sheet.cell(row=1, column=column_index, value=header)
            cell.font = Font(bold=True, color="FFFFFF")
            cell.fill = PatternFill("solid", fgColor="1F4E79")

    def _format(self, sheet: Worksheet) -> None:
        widths = {
            "A": 10,
            "B": 28,
            "C": 12,
            "D": 14,
            "E": 48,
            "F": 48,
        }
        for column, width in widths.items():
            sheet.column_dimensions[column].width = width
        sheet.freeze_panes = "A2"
        for row in sheet.iter_rows(min_row=2, max_col=6):
            for cell in row:
                alignment = copy(cell.alignment)
                alignment.wrap_text = True
                alignment.vertical = "top"
                cell.alignment = alignment
