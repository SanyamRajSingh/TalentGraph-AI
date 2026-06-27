import asyncio
import io
import uuid
import zipfile
from dataclasses import dataclass, field
from datetime import datetime

from app.pipelines.candidate_pipeline import CandidatePipeline


@dataclass
class BatchJobProgress:
    job_id: str
    total_files: int = 0
    processed_files: int = 0
    failed_files: int = 0
    status: str = "PENDING"
    created_at: datetime = field(default_factory=datetime.utcnow)
    completed_at: datetime | None = None
    errors: list[str] = field(default_factory=list)


class BatchPipeline:
    """Orchestrates async processing of batch uploads (e.g. ZIP files)."""

    def __init__(self, candidate_pipeline: CandidatePipeline) -> None:
        self.candidate_pipeline = candidate_pipeline
        # In-memory job state (for zero-infra background processing)
        self._jobs: dict[str, BatchJobProgress] = {}

    def get_job_status(self, job_id: str) -> BatchJobProgress | None:
        return self._jobs.get(job_id)

    async def upload_zip_async(self, file_bytes: bytes) -> str:
        """Starts a background task to process a ZIP file of resumes."""
        job_id = str(uuid.uuid4())
        
        try:
            with zipfile.ZipFile(io.BytesIO(file_bytes), "r") as z:
                # Filter out directories and hidden files (like __MACOSX)
                valid_files = [
                    name for name in z.namelist()
                    if not name.startswith("__MACOSX") 
                    and not name.startswith(".") 
                    and not name.endswith("/")
                ]
                
                job = BatchJobProgress(
                    job_id=job_id,
                    total_files=len(valid_files),
                    status="PROCESSING"
                )
                self._jobs[job_id] = job
                
                # We extract them into memory to pass to background task
                # (For very large zips, streaming would be better, but we do in-memory for MVP)
                files_data = [(name, z.read(name)) for name in valid_files]
                
        except zipfile.BadZipFile:
            job = BatchJobProgress(
                job_id=job_id,
                status="FAILED",
                errors=["Invalid ZIP file."]
            )
            self._jobs[job_id] = job
            return job_id

        # Fire and forget background processing
        asyncio.create_task(self._process_files_bg(job_id, files_data))
        return job_id

    async def _process_files_bg(self, job_id: str, files_data: list[tuple[str, bytes]]) -> None:
        """Background coroutine to parse and build digital twins from files."""
        job = self._jobs[job_id]
        
        for filename, file_bytes in files_data:
            try:
                # Dispatch to sync pipeline (wrapping in thread to avoid blocking event loop)
                await asyncio.to_thread(
                    self.candidate_pipeline.upload_from_file,
                    file_bytes=file_bytes,
                    filename=filename
                )
                job.processed_files += 1
            except Exception as e:
                job.failed_files += 1
                job.errors.append(f"{filename}: {str(e)}")
                
        job.status = "COMPLETED" if job.failed_files == 0 else "COMPLETED_WITH_ERRORS"
        job.completed_at = datetime.utcnow()
