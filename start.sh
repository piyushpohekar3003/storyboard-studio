#!/bin/bash
cd "$(dirname "$0")"

echo "================================"
echo "  Storyboard Studio"
echo "================================"
echo ""

# Check Python
if command -v python3 &>/dev/null; then
    PY=python3
elif command -v python &>/dev/null; then
    PY=python
else
    echo "Python 3 is required. Please install it from https://python.org"
    exit 1
fi

echo "Using: $($PY --version)"

# Create venv if needed
if [ ! -d "venv" ]; then
    echo "Setting up virtual environment..."
    $PY -m venv venv
fi

# Activate and install
source venv/bin/activate
echo "Installing dependencies..."
pip install -q -r requirements.txt

# Check for .env
if [ ! -f ".env" ]; then
    echo ""
    echo "No .env file found. Creating one..."
    read -p "Enter your Anthropic API key: " api_key
    echo "ANTHROPIC_API_KEY=$api_key" > .env
    echo ".env created."
fi

# Create data directory
mkdir -p data

echo ""
echo "Starting server at http://localhost:5000"
echo "Press Ctrl+C to stop."
echo ""
$PY app.py
