# Build GUI exe for Not a Culture Fit
param(
    [string]$ModelName = "llama3"
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path ".venv")) {
    py -m venv .venv
}

& .\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install requests pyinstaller

$env:NACF_MODEL = $ModelName

pyinstaller --onefile --windowed --name NotACultureFitGUI --clean src\nacf_ui.py

Write-Host "`nBuilt GUI at dist\NotACultureFitGUI.exe" -ForegroundColor Green
