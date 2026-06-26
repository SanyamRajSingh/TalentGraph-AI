from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class FeatureFlags(BaseSettings):
    """Feature flags used to keep hackathon increments explicit and reversible."""

    enable_role_dna_generator: bool = Field(default=False, alias="ENABLE_ROLE_DNA_GENERATOR")
    enable_candidate_twin_builder: bool = Field(default=False, alias="ENABLE_CANDIDATE_TWIN_BUILDER")
    enable_ranking_pipeline: bool = Field(default=False, alias="ENABLE_RANKING_PIPELINE")
    enable_graph_integration: bool = Field(default=False, alias="ENABLE_GRAPH_INTEGRATION")
    enable_embedding_engine: bool = Field(default=False, alias="ENABLE_EMBEDDING_ENGINE")

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


def get_feature_flags() -> FeatureFlags:
    """Dependency injection point for feature flag access."""

    return FeatureFlags()
