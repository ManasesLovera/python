@echo off
echo 🚀 ML Classification API Startup
echo ========================================

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.11+ and try again
    pause
    exit /b 1
)

REM Check if conda environment exists
conda info --envs | findstr "ml-classification-api" >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Conda environment 'ml-classification-api' not found
    echo Creating environment from environment.yml...
    conda env create -f environment.yml
    if errorlevel 1 (
        echo ❌ Failed to create conda environment
        pause
        exit /b 1
    )
)

REM Activate conda environment
echo 🔄 Activating conda environment...
call conda activate ml-classification-api
if errorlevel 1 (
    echo ❌ Failed to activate conda environment
    pause
    exit /b 1
)

REM Start the API
echo 🚀 Starting API server...
python start_api.py

pause
