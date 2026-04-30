@echo off
echo ==================================================
echo   Insider QA Project - Setup Environment
echo ==================================================

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH.
    pause
    exit /b %errorlevel%
)

:: Create Virtual Environment
echo [1/3] Creating virtual environment (.venv)...
python -m venv .venv

:: Activate and Install Requirements
echo [2/3] Installing dependencies from requirements.txt...
call .venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt

:: Create Reports directory
if not exist "reports" (
    echo [3/3] Creating reports directory...
    mkdir reports
)

echo ==================================================
echo   Setup Complete!
echo   To run tests, use: python run_tests.py
echo ==================================================
pause
