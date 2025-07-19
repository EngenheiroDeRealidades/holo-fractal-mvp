function Start-HoloAdmin {
    Start-Process powershell `
        -ArgumentList "-NoExit -Command `"cd 'D:\Site\holo-fractal-mvp'; Clear-Host; Write-Host 'HOLOFRACTAL DEV ENVIRONMENT' -ForegroundColor Magenta`"" `
        -Verb RunAs
}
