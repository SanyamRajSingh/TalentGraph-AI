from abc import ABC, abstractmethod

from app.domain.role_dna import RoleDNAProfile, RoleJob


class RoleDNARepository(ABC):
    """Persistence contract for job descriptions and Role DNA profiles."""

    @abstractmethod
    def save_job(self, job: RoleJob) -> RoleJob:
        """Persist a job description input."""

    @abstractmethod
    def get_job(self, job_id: str) -> RoleJob | None:
        """Fetch a job description input."""

    @abstractmethod
    def save(self, role_dna: RoleDNAProfile) -> RoleDNAProfile:
        """Persist a Role DNA profile."""

    @abstractmethod
    def get_by_role_id(self, role_id: str) -> RoleDNAProfile | None:
        """Fetch a Role DNA profile by role identifier."""

    @abstractmethod
    def list_role_dna(self) -> list[RoleDNAProfile]:
        """List persisted Role DNA profiles."""
