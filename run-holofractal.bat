@echo off
REM ─────────────────────────────────────────────────────────────
REM    HoloFractal MVP Launcher — Diagnóstico & Ativação Visual
REM ─────────────────────────────────────────────────────────────
echo ================================
echo 💀 INICIANDO HOLOFRACTAL SYSTEM
echo ================================
echo.

REM ⚙️ Base folder (onde este .bat está)
set "BASE_DIR=%~dp0"

REM 🐍 Verifica se o venv está presente
if not exist "%BASE_DIR%\.venv\Scripts\activate.bat" (
    echo ❌ Ambiente virtual não encontrado em: %BASE_DIR%\.venv\Scripts\
    pause
    exit /b
)

REM 🔄 Backend FastAPI
start "🔧 Backend FastAPI" cmd /k ^
    ""%BASE_DIR%\.venv\Scripts\activate.bat" && echo 🟢 VENV: %VIRTUAL_ENV% && cd /d "%BASE_DIR%backend" && uvicorn main:app --reload"

REM 🎯 Frontend Streamlit
start "📊 Dashboard Streamlit" cmd /k ^
    ""%BASE_DIR%\.venv\Scripts\activate.bat" && echo 🟢 VENV: %VIRTUAL_ENV% && cd /d "%BASE_DIR%frontend" && streamlit run app.py"

REM 🔭 Script Astronômico
start "🔮 Script Astro.py" cmd /k ^
    ""%BASE_DIR%\.venv\Scripts\activate.bat" && echo 🟢 VENV: %VIRTUAL_ENV% && cd /d "%BASE_DIR%scripts" && python astro.py"

echo.
echo ✅ Três janelas CMD foram abertas com venv ativado.
pause
