from app.domain.role_dna import RoleDNAProfile, RoleJob
from app.repositories.role_dna_repository import RoleDNARepository


class InMemoryRoleDNARepository(RoleDNARepository):
    """Process-local Role DNA repository for tests and hackathon demo runs."""

    def __init__(self) -> None:
        self._jobs: dict[str, RoleJob] = {}
        self._role_dna: dict[str, RoleDNAProfile] = {}

    def save_job(self, job: RoleJob) -> RoleJob:
        self._jobs[job.job_id] = job
        return job

    def get_job(self, job_id: str) -> RoleJob | None:
        return self._jobs.get(job_id)

    def save(self, role_dna: RoleDNAProfile) -> RoleDNAProfile:
        self._role_dna[role_dna.role_id] = role_dna
        return role_dna

    def get_by_role_id(self, role_id: str) -> RoleDNAProfile | None:
        return self._role_dna.get(role_id)

    def list_role_dna(self) -> list[RoleDNAProfile]:
        return list(self._role_dna.values())
