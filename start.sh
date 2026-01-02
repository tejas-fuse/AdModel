#!/bin/bash

# AdModel Startup Script

echo "🎨 Starting AdModel - AI Virtual Model Creator"
echo "=============================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -q -r requirements.txt

# Create necessary directories
mkdir -p uploads saved_models

# Start the server
echo ""
echo "🚀 Starting AdModel server..."
echo "📍 Access the application at: http://localhost:8000"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
