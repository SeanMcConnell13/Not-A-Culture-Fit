param(
  [string]$Python = "python",
  [switch]$Clean
)

$ErrorActionPreference = "Stop"

if ($Clean) {
  if (Test-Path build) { Remove-Item build -Recurse -Force }
  if (Test-Path dist) { Remove-Item dist -Recurse -Force }
  if (Test-Path __pycache__) { Remove-Item __pycache__ -Recurse -Force }
}

# Ensure deps
& $Python -m pip install --upgrade pip
& $Python -m pip install -r requirements.txt pyinstaller

# Build
Write-Host ">> Packing NotACultureFitGUI.exe..." -ForegroundColor Cyan
pyinstaller --clean --noconfirm not_a_culture_fit.spec

Write-Host "`nBuild complete:" -ForegroundColor Green
Get-ChildItem dist\ -Recurse | Where-Object {$_.Extension -in ".exe",".dll"} | Format-Table Length, FullName
