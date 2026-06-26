from app.domain.ranking import HiringPersona
from app.modules.recruiter_brain.persona_engine import PersonaEngine


class WeightRegistry:
    """Provides persona-specific scoring weights."""

    def __init__(self, persona_engine: PersonaEngine | None = None) -> None:
        self.persona_engine = persona_engine or PersonaEngine()

    def get_weights(self, persona: HiringPersona) -> dict[str, int]:
        return self.persona_engine.get_weights(persona)
