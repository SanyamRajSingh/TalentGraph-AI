from typing import Protocol

from app.domain.role_dna import RoleDNAProfile, RoleJob
from app.events import JobUploaded, RoleDNAGenerated
from app.repositories.role_dna_repository import RoleDNARepository


class RoleDNAService(Protocol):
    """Dependency boundary for Role DNA generation."""

    def generate(self, job_description: str, job_id: str | None = None) -> RoleDNAProfile:
        """Generate a normalized Role DNA profile."""


class RoleRepository(Protocol):
    """Persistence boundary for jobs and Role DNA records."""

    def save_role_dna(self, role_dna: RoleDNAProfile) -> RoleDNAProfile:
        """Persist a Role DNA profile."""


class RolePipeline:
    """Orchestrates job upload through Role DNA generation."""

    def __init__(
        self,
        role_dna_service: RoleDNAService,
        role_repository: RoleDNARepository,
    ) -> None:
        self.role_dna_service = role_dna_service
        self.role_repository = role_repository

    def upload_job(self, job_description: str, source_name: str | None = None) -> tuple[RoleJob, JobUploaded]:
        job = self.role_repository.save_job(
            RoleJob(job_description=job_description, source_name=source_name)
        )
        return job, JobUploaded(job_id=job.job_id)

    def run(self, job_description: str, job_id: str | None = None) -> tuple[RoleDNAProfile, RoleDNAGenerated]:
        if job_id:
            job = self.role_repository.get_job(job_id)
            if job is None:
                raise ValueError(f"Job {job_id} was not found.")
            job_description = job.job_description
        else:
            job, _ = self.upload_job(job_description=job_description)
            job_id = job.job_id

        role_dna = self.role_dna_service.generate(job_description, job_id=job_id)
        saved = self.role_repository.save(role_dna)
        return saved, RoleDNAGenerated(role_id=saved.role_id)
