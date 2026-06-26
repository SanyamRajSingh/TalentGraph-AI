from pydantic import BaseModel

from app.domain.evaluation import EvaluationBundle


class EvaluationResponse(BaseModel):
    evaluation_id: str
    evaluation: EvaluationBundle
