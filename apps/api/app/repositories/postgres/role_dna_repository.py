from sqlalchemy.orm import Session

from app.domain.role_dna import RoleDNAProfile, RoleJob
from app.repositories.role_dna_repository import RoleDNARepository


class PostgresRoleDNARepository(RoleDNARepository):
    """PostgreSQL Role DNA repository skeleton.

    Concrete table mappings and migrations are intentionally deferred until
    persistence hardening. Module 1 uses the repository interface and in-memory
    implementation for testable demo behavior.
    """

    def __init__(self, session: Session) -> None:
        self.session = session

    def save_job(self, job: RoleJob) -> RoleJob:
        raise NotImplementedError("PostgreSQL job persistence is not implemented in Module 1.")

    def get_job(self, job_id: str) -> RoleJob | None:
        raise NotImplementedError("PostgreSQL job lookup is not implemented in Module 1.")

    def save(self, role_dna: RoleDNAProfile) -> RoleDNAProfile:
        raise NotImplementedError("PostgreSQL Role DNA persistence is not implemented in Module 1.")

    def get_by_role_id(self, role_id: str) -> RoleDNAProfile | None:
        raise NotImplementedError("PostgreSQL Role DNA lookup is not implemented in Module 1.")

    def list_role_dna(self) -> list[RoleDNAProfile]:
        raise NotImplementedError("PostgreSQL Role DNA listing is not implemented in Module 1.")
