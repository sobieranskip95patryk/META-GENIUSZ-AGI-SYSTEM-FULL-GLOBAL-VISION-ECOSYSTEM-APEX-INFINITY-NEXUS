#!/bin/bash
# GOK:AI Development Environment Setup Script
# Platform: Linux/macOS
# Purpose: Initialize development environment with all dependencies

set -e

echo "=========================================="
echo "GOK:AI Development Environment Setup"
echo "=========================================="

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Step 1: Create virtual environment
echo -e "${BLUE}[1/6]${NC} Creating Python virtual environment..."
python3 -m venv .venv
source .venv/bin/activate

# Step 2: Upgrade pip
echo -e "${BLUE}[2/6]${NC} Upgrading pip..."
pip install --upgrade pip setuptools wheel

# Step 3: Install main dependencies
echo -e "${BLUE}[3/6]${NC} Installing main dependencies..."
pip install -r requirements.txt

# Step 4: Install MTAQUEST dependencies
if [ -f "MTAQUEST/requirements.txt" ]; then
  echo -e "${BLUE}[4/6]${NC} Installing MTAQUEST dependencies..."
  pip install -r MTAQUEST/requirements.txt
else
  echo -e "${YELLOW}[4/6]${NC} MTAQUEST/requirements.txt not found (skipping)"
fi

# Step 5: Install development dependencies
echo -e "${BLUE}[5/6]${NC} Installing development tools..."
pip install pytest pytest-cov black isort flake8 mypy

# Step 6: Create .env file if it doesn't exist
echo -e "${BLUE}[6/6]${NC} Setting up environment configuration..."
if [ ! -f ".env" ]; then
  if [ -f ".env.example" ]; then
    cp .env.example .env
    echo -e "${YELLOW}Created .env file from template${NC}"
    echo -e "${YELLOW}⚠️  Please edit .env with your API keys and configuration${NC}"
  fi
fi

echo ""
echo -e "${GREEN}=========================================="
echo "✅ Setup Complete!"
echo "==========================================${NC}"
echo ""
echo "To activate the environment, run:"
echo -e "${BLUE}source .venv/bin/activate${NC}"
echo ""
echo "To start the application, run:"
echo -e "${BLUE}python main.py${NC}"
echo ""
echo "To run tests, use:"
echo -e "${BLUE}pytest tests/${NC}"
echo ""
