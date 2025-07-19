# 🔮 Configuração
$base   = "D:\Site\holo-fractal-mvp"
$venv   = "$base\.venv\Scripts\Activate.ps1"
$logDir = "$base\logs"
$ErrorActionPreference = "Continue"
if (-not (Test-Path $logDir)) { New-Item $logDir -ItemType Directory | Out-Null }

# 🎬 Cascata mística estilo Matrix
function Invoke-FractalCascade {
    $charset = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#$%^&*"
    $columns = 40; $height = 25
    $positions = @(0) * $columns
    for ($frame = 0; $frame -lt 80; $frame++) {
        Clear-Host
        for ($row = 0; $row -lt $height; $row++) {
            $line = ""
            for ($col = 0; $col -lt $columns; $col++) {
                $line += if ($positions[$col] -eq $row) { 
                    "$($charset[(Get-Random -Maximum $charset.Length)]) " 
                } else { "  " }
            }
            Write-Host $line -ForegroundColor DarkGreen
        }
        for ($i = 0; $i -lt $columns; $i++) {
            if ((Get-Random -Maximum 10) -gt 7) {
                $positions[$i] = ($positions[$i] + 1) % $height
            }
        }
        Start-Sleep -Milliseconds 70
    }
    Write-Host "`n🌀 Portal HoloFractal aberto..." -ForegroundColor Cyan
    Start-Sleep -Seconds 1
}

Invoke-FractalCascade

# 🔁 Módulo de invocação
function Start-FractalJob {
    param ($title, $folder, $command)
    $script = @"
`$env:VIRTUAL_ENV = '$base\.venv'
& '$venv'
cd '$folder'
$command
"@
    try {
        $job = Start-Job -ScriptBlock ([ScriptBlock]::Create($script))
        return @{Name=$title; Job=$job; Status="OK"; Message="Job iniciado"}
    } catch {
        return @{Name=$title; Job=$null; Status="ERRO"; Message="Falha: $_"}
    }
}

# 🌐 Verificar /health
function Test-BackendHealth {
    try {
        $resp = Invoke-WebRequest -Uri "http://127.0.0.1:8000/health" -UseBasicParsing -TimeoutSec 2
        $status = ($resp.Content | ConvertFrom-Json).status
        $color = if ($status -eq "ok") { "Green" } else { "Red" }
        Write-Host "🔍 Backend /health: $status" -ForegroundColor $color
    } catch {
        Write-Host "❌ Backend /health: sem resposta" -ForegroundColor Red
    }
}

# 🧪 POST para /configure
function Test-Configure {
    $body = @{
        goals = @("cura", "prosperidade")
        priority_keys = @(1, 3)
    } | ConvertTo-Json -Depth 3

    try {
        $resp = Invoke-WebRequest -Method POST `
            -Uri "http://127.0.0.1:8000/configure" `
            -Body $body `
            -ContentType "application/json"
        $json = $resp.Content | ConvertFrom-Json
        Write-Host "✅ /configure: Session ID = $($json.session_id)" -ForegroundColor Cyan
    } catch {
        Write-Host "❌ Falha ao enviar /configure" -ForegroundColor Red
    }
}

# 🎛️ Painel interativo
$services = @()
do {
    Write-Host "`n🧙‍♂️ Escolha sua invocação:" -ForegroundColor Cyan
    Write-Host "[1] Iniciar Backend"
    Write-Host "[2] Iniciar Frontend"
    Write-Host "[3] Rodar Astro Script"
    Write-Host "[4] Verificar status dos módulos"
    Write-Host "[5] Testar /health do Backend"
    Write-Host "[6] Enviar payload para /configure"
    Write-Host "[7] Encerrar todos os serviços"
    Write-Host "[0] Sair do Portal"
    $op = Read-Host "Digite sua opção"

    switch ($op) {
        "1" {
            $services += Start-FractalJob -title "Backend" -folder "$base\backend" -command "uvicorn main:app --reload"
            Write-Host "✅ Backend iniciado!" -ForegroundColor Green
        }
        "2" {
            $services += Start-FractalJob -title "Frontend" -folder "$base\frontend" -command "streamlit run app.py"
            Write-Host "✅ Frontend iniciado!" -ForegroundColor Green
        }
        "3" {
            $services += Start-FractalJob -title "Astro" -folder "$base\scripts" -command "python astro.py"
            Write-Host "✅ Script Astro em execução." -ForegroundColor Green
        }
        "4" {
            foreach ($svc in $services) {
                $job = $svc.Job
                if ($job) {
                    $state = (Get-Job -Id $job.Id).State
                    $statusText = if ($state -eq "Running") { "🟢 Rodando" } elseif ($state -eq "Completed") { "⚪ Finalizado" } elseif ($state -eq "Failed") { "🔴 Falhou" } else { "🟡 $state" }
                    Write-Host "$($svc.Name): $statusText"
                } else {
                    Write-Host "$($svc.Name): ❌ Não iniciado"
                }
            }
        }
        "5" { Test-BackendHealth }
        "6" { Test-Configure }
        "7" {
            Write-Host "⛔ Encerrando todos os serviços..."
            foreach ($svc in $services) {
                if ($svc.Job) { Stop-Job -Job $svc.Job -Force }
            }
            $services = @()
        }
        "0" {
            Write-Host "💠 Encerrando o portal..." -ForegroundColor DarkGray
            break
        }
        default {
            Write-Host "Opção inválida." -ForegroundColor Red
        }
    }

    Write-Host "`n🔁 Retornando ao menu..."
    Start-Sleep -Seconds 1
} while ($true)
