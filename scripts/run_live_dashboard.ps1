# Run the live prototype dashboard (Windows PowerShell)
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $Root

if (-not (Test-Path ".venv\Scripts\python.exe")) {
    python -m venv .venv
}

& .\.venv\Scripts\python.exe -m pip install -r requirements.txt --quiet
& .\.venv\Scripts\python.exe scripts/prepare_week1_data.py
& .\.venv\Scripts\python.exe scripts/prepare_energy_data.py

Write-Host "Starting live dashboard at http://localhost:8501"
& .\.venv\Scripts\python.exe -m streamlit run streamlit_app.py
