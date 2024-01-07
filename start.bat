@echo off

REM Checking the presence of a virtual environment
if not exist "venv" (
    echo Creating a virtual environment...
    python -m venv venv
)

REM Activating the virtual environment
echo Activating the virtual environment..
call venv\Scripts\activate.bat

REM Installing dependencies
echo Installing dependencies from the requirements.txt file...
pip install -r requirements.txt

REM Launching the application
echo Launching the application...
python app.py

REM Deactivating a virtual environment
call venv\Scripts\deactivate.bat
