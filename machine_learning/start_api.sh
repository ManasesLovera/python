#!/bin/bash

echo "🚀 ML Classification API Startup"
echo "========================================"

# Check if Python is available
if ! command -v python &> /dev/null; then
    echo "❌ Python is not installed or not in PATH"
    echo "Please install Python 3.11+ and try again"
    exit 1
fi

# Check if conda is available
if command -v conda &> /dev/null; then
    echo "🔄 Using conda environment..."
    
    # Check if conda environment exists
    if ! conda info --envs | grep -q "ml-classification-api"; then
        echo "⚠️  Conda environment 'ml-classification-api' not found"
        echo "Creating environment from environment.yml..."
        conda env create -f environment.yml
        if [ $? -ne 0 ]; then
            echo "❌ Failed to create conda environment"
            exit 1
        fi
    fi
    
    # Activate conda environment
    echo "🔄 Activating conda environment..."
    source $(conda info --base)/etc/profile.d/conda.sh
    conda activate ml-classification-api
    if [ $? -ne 0 ]; then
        echo "❌ Failed to activate conda environment"
        exit 1
    fi
else
    echo "⚠️  Conda not found, using system Python"
    echo "Make sure dependencies are installed: pip install -r requirements.txt"
fi

# Start the API
echo "🚀 Starting API server..."
python start_api.py
