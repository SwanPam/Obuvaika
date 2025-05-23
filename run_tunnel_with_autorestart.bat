@echo off
chcp 65001 > nul
set MAX_RETRIES=5
set RETRY_DELAY=5
set retry_count=0

:main_loop
echo [%time%] Starting local tunnel on port 8000 (attempt %retry_count%/%MAX_RETRIES%)...
lt --port 8000

if %errorlevel% neq 0 (
    set /a retry_count+=1
    if %retry_count% geq %MAX_RETRIES% (
        echo [ERROR] Maximum retry attempts reached (%MAX_RETRIES%)
        pause
        exit /b 1
    )
    
    echo [ERROR] Tunnel crashed, restarting in %RETRY_DELAY% seconds...
    timeout /t %RETRY_DELAY% /nobreak > nul
    echo ======= RESTARTING =======
    
    rem Increase delay with each attempt
    set /a RETRY_DELAY+=2
    
    call :main_loop
) else (
    echo Tunnel terminated successfully
    pause
    exit /b 0
)

:end