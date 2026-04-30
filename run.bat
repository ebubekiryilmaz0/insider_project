@echo off
:: Activate virtual environment if it exists
if exist ".venv\Scripts\activate.bat" (
    call .venv\Scripts\activate.bat
)

:: Forward all arguments to the python runner
python run_tests.py %*
