param(
    [string]$ModelName = "llama3"
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path ".venv")) {
    py -m venv .venv
}

# Activate venv
& .\.venv\Scripts\Activate.ps1

python -m pip install --upgrade pip
pip install -r requirements.txt pyinstaller

# optional: pass model name for local run
$env:NACF_MODEL = $ModelName

# Build one-file exe
pyinstaller --onefile --name NotACultureFit --clean src/not_a_culture_fit.py

Write-Host "`nBuilt EXE at dist\NotACultureFit.exe" -ForegroundColor Green
