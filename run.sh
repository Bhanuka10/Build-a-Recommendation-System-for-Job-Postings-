#!/usr/bin/env bash
# Startup script for Job Recommendation System Web App
# This script handles all setup and runs the application

echo "================================================"
echo "Job Recommendation System - Web Application"
echo "================================================"
echo ""

# Check Python installation
echo "Checking Python installation..."
if ! command -v python &> /dev/null; then
    echo "✗ Python not found. Please install Python 3.7+"
    exit 1
fi
echo "✓ Python found"

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo ""
    echo "Creating virtual environment..."
    python -m venv .venv
    echo "✓ Virtual environment created"
fi

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source .venv/bin/activate
echo "✓ Virtual environment activated"

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install -r requirements.txt -q
echo "✓ Dependencies installed"

# Test the engine
echo ""
echo "Testing recommendation engine..."
python test_webapp.py
test_result=$?

if [ $test_result -eq 0 ]; then
    echo ""
    echo "================================================"
    echo "Starting web application..."
    echo "================================================"
    echo ""
    echo "The application will be available at:"
    echo "  → http://localhost:5000"
    echo ""
    echo "Press Ctrl+C to stop the application"
    echo ""
    
    python app.py
else
    echo ""
    echo "✗ Engine test failed. Please check configuration."
    exit 1
fi
