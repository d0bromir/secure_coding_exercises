<#
  setup-class-windows.ps1
  Usage (Admin PowerShell): .\setup-class-windows.ps1
  Това прави:
    - инсталира Git, Visual Studio Build Tools 2022, Python 3 и PyCharm с Chocolatey
    - настройва системен PATH за python, проверява pip
    - създава примерна виртуална среда
#>

Set-StrictMode -Version Latest

function Write-Info($m){ Write-Host "[INFO] $m" -ForegroundColor Cyan }
function Write-Warn($m){ Write-Host "[WARN] $m" -ForegroundColor Yellow }
function Write-Err($m){ Write-Host "[ERROR] $m" -ForegroundColor Red }

# ---- Config ----
$installPyCharm = $true
$create_example_venv = $true
# -----------------

# Ensure running as admin
$cur = [Security.Principal.WindowsIdentity]::GetCurrent()
$principal = New-Object Security.Principal.WindowsPrincipal($cur)
if (-not $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    Write-Warn "This script must be run as Administrator. Re-run PowerShell as Administrator and try again."
    exit 2
}

$choco = (Get-Command choco -ErrorAction SilentlyContinue)
if (-not $choco) {
    Write-Info "Chocolatey not found. Installing Chocolatey..."
    Set-ExecutionPolicy Bypass -Scope Process -Force
    $chocoScript = "Set-ExecutionPolicy Bypass -Scope Process -Force; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))"
    iex $chocoScript
}
Write-Info "Using choco for installations..."
choco feature enable -n allowGlobalConfirmation
choco install git -y
choco install visualstudio2022buildtools -y --package-parameters "--includeRecommended --add Microsoft.VisualStudio.Workload.VCTools --add Microsoft.VisualStudio.Component.Windows10SDK.19041"
choco install python -y
if ($installPyCharm) { choco install pycharm -y }


# Ensure python is on PATH now
$py = (Get-Command python -ErrorAction SilentlyContinue)
if (-not $py) {
    Write-Warn "Python not found on PATH. Trying python3..."
    $py = (Get-Command python3 -ErrorAction SilentlyContinue)
}
if (-not $py) {
    Write-Err "Python still not found. Please ensure Python is installed and added to PATH. Exiting."
    exit 3
}
Write-Info "Python binary: $($py.Path)"

# Upgrade pip and install useful packages
Write-Info "Upgrading pip and installing virtualenv..."
& $py.Path -m pip install --upgrade pip setuptools wheel virtualenv

choco install mingw -y
$envPath = [Environment]::GetEnvironmentVariable('Path', 'Machine')
$new = $envPath + ';C:\ProgramData\chocolatey\lib\mingw\tools\install\mingw64\bin'
[Environment]::SetEnvironmentVariable('Path', $new, 'Machine')


Write-Info "Installation finished. Please reboot systems if required."
