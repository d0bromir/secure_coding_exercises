<#
  setup-class-windows-intro.ps1
  Usage (Admin PowerShell): .\setup-class-windows-intro.ps1
  Това прави:
    - премахва Git, Python 3 и PyCharm с Chocolatey
#>

Set-StrictMode -Version Latest

function Write-Info($m){ Write-Host "[INFO] $m" -ForegroundColor Cyan }
function Write-Warn($m){ Write-Host "[WARN] $m" -ForegroundColor Yellow }
function Write-Err($m){ Write-Host "[ERROR] $m" -ForegroundColor Red }


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
choco feature enable -n=allowGlobalConfirmation
choco uninstall git -y --all-versions --remove-dependencies
choco uninstall python -y --all-versions --remove-dependencies
choco uninstall pycharm -y --all-versions --remove-dependencies


Write-Info "Setup finished. Please reboot systems if required."
