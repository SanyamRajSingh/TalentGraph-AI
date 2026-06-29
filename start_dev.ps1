$ErrorActionPreference = "Stop"

Write-Host "Starting TalentGraph AI Local Environment..." -ForegroundColor Green

# Ensure backend virtual environment is used
$BackendScript = {
    Write-Host "Starting FastAPI Backend (Port 8000)..." -ForegroundColor Cyan
    Set-Location -Path "apps\api"
    # Fallback to copy .env if it doesn't exist
    if (-not (Test-Path ".env")) {
        Copy-Item -Path "..\..\.env.development" -Destination ".env" -ErrorAction SilentlyContinue
    }
    # Run uvicorn via the virtual environment
    & "..\..\.venv\Scripts\python.exe" -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
}

# Start Frontend
$FrontendScript = {
    Write-Host "Starting Next.js Frontend (Port 3000)..." -ForegroundColor Yellow
    # Create web .env.local if missing
    if (-not (Test-Path "apps\web\.env.local")) {
        [IO.File]::WriteAllText("$PWD\apps\web\.env.local", "NEXT_PUBLIC_API_BASE_URL=http://localhost:8000")
    }
    npm run dev:web
}

# Start processes
Write-Host "Press Ctrl+C to stop both servers." -ForegroundColor Magenta
$BackendJob = Start-Job -ScriptBlock $BackendScript -WorkingDirectory $PWD
$FrontendJob = Start-Job -ScriptBlock $FrontendScript -WorkingDirectory $PWD

try {
    # Stream logs to console
    while ($true) {
        Receive-Job -Job $BackendJob
        Receive-Job -Job $FrontendJob
        Start-Sleep -Milliseconds 500
    }
}
finally {
    Write-Host "`nStopping servers..." -ForegroundColor Red
    Stop-Job -Job $BackendJob, $FrontendJob
    Remove-Job -Job $BackendJob, $FrontendJob
}
