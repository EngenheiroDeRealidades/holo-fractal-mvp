New-Item -Path "D:\Site\holo-fractal-mvp" -Name "admin-shell.ps1" -ItemType "file" -Value @"
if (-NOT ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Start-Process powershell -ArgumentList "-NoExit -Command `"cd '$PSScriptRoot'; & '$PSCommandPath'`"" -Verb RunAs
    Exit
}
Set-Location $PSScriptRoot
Write-Host "PowerShell Admin na pasta do projeto - HoloFractal OS" -ForegroundColor Cyan
"@