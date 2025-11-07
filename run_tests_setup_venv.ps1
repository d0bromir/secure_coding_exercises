
param([switch]$SkipVuln)
$ErrorActionPreference = "Stop"
function Info($m){ Write-Host "[INFO] $m" -ForegroundColor Cyan }
function Ok($m){ Write-Host "[OK] $m" -ForegroundColor Green }
function Warn($m){ Write-Host "[WARN] $m" -ForegroundColor Yellow }
function Err($m){ Write-Host "[ERROR] $m" -ForegroundColor Red }
$pythonGlobal = (Get-Command python -ErrorAction SilentlyContinue)
if (-not $pythonGlobal) { Err "Python not found"; exit 1 }
Info "Using global python: $($pythonGlobal.Path)"
$venvPython = ".\.venv\Scripts\python.exe"
if (-not (Test-Path $venvPython)) {
  Info "Creating .venv"
  & $pythonGlobal.Path -m venv .venv
  Ok ".venv created"
} else { Info ".venv exists" }
Info "Upgrading pip in venv..."
& $venvPython -m pip install --upgrade pip setuptools wheel
if (Test-Path "requirements.txt") {
  Info "Installing from requirements.txt..."
  & $venvPython -m pip install -r requirements.txt
} else {
  Info "No requirements.txt, installing minimal deps"
  & $venvPython -m pip install pytest flask
}
Info "Cleaning __pycache__ and .pyc files..."
Get-ChildItem -Path . -Recurse -Force -Include "__pycache__" -ErrorAction SilentlyContinue | ForEach-Object { Remove-Item $_.FullName -Recurse -Force -ErrorAction SilentlyContinue }
Get-ChildItem -Path . -Recurse -Force -Filter "*.pyc" -ErrorAction SilentlyContinue | ForEach-Object { Remove-Item $_.FullName -Force -ErrorAction SilentlyContinue }
Info "Discovering test files..."
$testFiles = Get-ChildItem -Path . -Recurse -Filter "test_*.py" | Select-Object -ExpandProperty FullName
if ($testFiles.Count -eq 0) { Warn "No test_*.py files found. Exiting."; exit 0 }
$funcs = $testFiles | Where-Object { $_ -match "test_functional" }
$vulns = $testFiles | Where-Object { $_ -match "test_vuln" }
if ($funcs.Count -gt 0) {
  Info "Running functional tests..."
  & $venvPython -m pytest -q --disable-warnings @($funcs) -continue-on-collection-errors
} else { Info "No functional tests found" }
if (-not $SkipVuln) {
  if ($vulns.Count -gt 0) {
    Info "Running vulnerability tests..."
    & $venvPython -m pytest -q --disable-warnings @($vulns) -continue-on-collection-errors
  } else { Info "No vulnerability tests found" }
} else { Info "Skipping vuln tests by flag" }

Ok "Done"
