@echo off

py -c "import fastapi, uvicorn, lso" >nul 2>&1

if errorlevel 1 (
    echo First-time setup: installing required packages...
    py -m pip install -e .

    if errorlevel 1 (
        echo.
        echo Setup failed.
        pause
        exit /b 1
    )
)

echo Starting Living Systems Observatory...

start "" cmd /c "timeout /t 2 /nobreak >nul & start http://127.0.0.1:8000/docs"

py -m uvicorn lso.main:app

if errorlevel 1 (
    echo.
    echo Something went wrong.
    pause
)
