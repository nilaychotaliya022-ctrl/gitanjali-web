@echo off
setlocal
title Gitanjali Website - Setup

echo ==========================================
echo   GITANJALI WEBSITE - FIRST TIME SETUP
echo ==========================================
echo.

set "PYTHON=%LocalAppData%\Programs\Python\Python311\python.exe"

if not exist "%PYTHON%" (
    echo Python 3.11 was not found at:
    echo %PYTHON%
    echo.
    echo Please install Python 3.11, then run this file again.
    pause
    exit /b 1
)

echo [1/5] Checking Python...
"%PYTHON%" --version
if errorlevel 1 goto :error

echo.
echo [2/5] Installing/updating required packages...
"%PYTHON%" -m pip install -r requirements.txt
if errorlevel 1 goto :error

echo.
echo [3/5] Applying database migrations...
"%PYTHON%" manage.py migrate
if errorlevel 1 goto :error

echo.
echo [4/5] Loading demo/product data if the seed command is available...
"%PYTHON%" manage.py seed_products
if errorlevel 1 (
    echo.
    echo Seed command returned an error. Continuing because migrations completed.
)

echo.
echo [5/5] Running Django system check...
"%PYTHON%" manage.py check
if errorlevel 1 goto :error

echo.
echo ==========================================
echo   SETUP COMPLETE
echo ==========================================
echo.
echo Starting the website at:
echo http://127.0.0.1:8000/
echo.
echo Keep this window open while using the site.
echo Press CTRL+C to stop the server.
echo.
"%PYTHON%" manage.py runserver 127.0.0.1:8000
exit /b 0

:error
echo.
echo ==========================================
echo   SETUP FAILED
echo ==========================================
echo Read the error above and send it to ChatGPT.
pause
exit /b 1
