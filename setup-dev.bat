@echo off
REM GOK:AI Development Environment Setup Script
REM Platform: Windows
REM Purpose: Initialize development environment with all dependencies

setlocal enabledelayedexpansion

echo.
echo ==========================================
echo GOK:AI Development Environment Setup
echo ==========================================
echo.

REM Step 1: Create virtual environment
echo [1/6] Creating Python virtual environment...
python -m venv .venv
if errorlevel 1 (
    echo Error creating virtual environment
    exit /b 1
)

REM Step 2: Activate virtual environment
call .venv\Scripts\activate.bat
if errorlevel 1 (
    echo Error activating virtual environment
    exit /b 1
)

REM Step 3: Upgrade pip
echo [2/6] Upgrading pip...
python -m pip install --upgrade pip setuptools wheel

REM Step 4: Install main dependencies
echo [3/6] Installing main dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo Error installing main dependencies
    exit /b 1
)

REM Step 5: Install MTAQUEST dependencies
if exist "MTAQUEST\requirements.txt" (
    echo [4/6] Installing MTAQUEST dependencies...
    pip install -r MTAQUEST\requirements.txt
) else (
    echo [4/6] MTAQUEST\requirements.txt not found ^(skipping^)
)

REM Step 6: Install development dependencies
echo [5/6] Installing development tools...
pip install pytest pytest-cov black isort flake8 mypy

REM Step 7: Create .env file if it doesn't exist
echo [6/6] Setting up environment configuration...
if not exist ".env" (
    if exist ".env.example" (
        copy .env.example .env
        echo Created .env file from template
        echo WARNING: Please edit .env with your API keys and configuration
    )
)

echo.
echo ==========================================
echo ^!~== Setup Complete ==~!
echo ==========================================
echo.
echo Your Python environment is now ready!
echo.
echo To start the application, run:
echo   python main.py
echo.
echo To run tests, use:
echo   pytest tests\
echo.
echo To use Docker instead, run:
echo   docker-compose up
echo.
pause
