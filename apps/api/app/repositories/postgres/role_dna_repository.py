"""PostgreSQL implementation of RoleDNARepository."""

from sqlalchemy.orm import Session

from app.db.models import JobRow, RoleDNARow
from app.domain.role_dna import RoleDNAProfile, RoleJob
from app.repositories.role_dna_repository import RoleDNARepository


class PostgresRoleDNARepository(RoleDNARepository):
    """PostgreSQL-backed Role DNA repository using SQLAlchemy ORM."""

    def __init__(self, session: Session) -> None:
        self.session = session

    # ------------------------------------------------------------------ jobs

    def save_job(self, job: RoleJob) -> RoleJob:
        existing = self.session.query(JobRow).filter_by(job_id=job.job_id).first()
        if existing:
            existing.payload = job.model_dump(mode="json")
            existing.source_name = job.source_name
        else:
            row = JobRow(
                job_id=job.job_id,
                source_name=job.source_name,
                payload=job.model_dump(mode="json"),
            )
            self.session.add(row)
        self.session.commit()
        return job

    def get_job(self, job_id: str) -> RoleJob | None:
        row = self.session.query(JobRow).filter_by(job_id=job_id).first()
        if row is None:
            return None
        return RoleJob.model_validate(row.payload)

    # ------------------------------------------------------------------ role DNA

    def save(self, role_dna: RoleDNAProfile) -> RoleDNAProfile:
        existing = self.session.query(RoleDNARow).filter_by(role_id=role_dna.role_id).first()
        payload = role_dna.model_dump(mode="json")
        if existing:
            existing.role_title = role_dna.role_title
            existing.domain = role_dna.domain
            existing.seniority = role_dna.seniority
            existing.job_id = role_dna.job_id
            existing.payload = payload
        else:
            row = RoleDNARow(
                role_id=role_dna.role_id,
                job_id=role_dna.job_id,
                role_title=role_dna.role_title,
                domain=role_dna.domain,
                seniority=role_dna.seniority,
                payload=payload,
            )
            self.session.add(row)
        self.session.commit()
        return role_dna

    def get_by_role_id(self, role_id: str) -> RoleDNAProfile | None:
        row = self.session.query(RoleDNARow).filter_by(role_id=role_id).first()
        if row is None:
            return None
        return RoleDNAProfile.model_validate(row.payload)

    def list_role_dna(self) -> list[RoleDNAProfile]:
        rows = self.session.query(RoleDNARow).order_by(RoleDNARow.created_at.desc()).all()
        return [RoleDNAProfile.model_validate(r.payload) for r in rows]
