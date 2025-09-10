#!/usr/bin/env python3
"""
Startup script for ML Classification API
Handles environment setup, model training, and API startup
"""
import os
import sys
import subprocess
from pathlib import Path

def check_environment():
    """Check if the environment is properly set up"""
    print("🔍 Checking environment...")
    
    # Check if required files exist
    required_files = [
        "app.py",
        "config.py", 
        "requirements.txt",
        "data/dataset.json"
    ]
    
    missing_files = []
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Missing required files: {missing_files}")
        return False
    
    print("✅ Environment check passed")
    return True

def check_dependencies():
    """Check if required dependencies are installed"""
    print("🔍 Checking dependencies...")
    
    try:
        import fastapi
        import uvicorn
        import pandas
        import sklearn
        import joblib
        print("✅ All dependencies are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please install dependencies with: pip install -r requirements.txt")
        return False

def check_model():
    """Check if model is trained and available"""
    print("🔍 Checking model...")
    
    model_path = Path("saved_models/svm")
    if model_path.exists() and (model_path / "model.pkl").exists():
        print("✅ SVM model is available")
        return True
    else:
        print("⚠️  SVM model not found")
        return False

def train_model():
    """Train the SVM model"""
    print("🤖 Training SVM model...")
    
    try:
        result = subprocess.run([sys.executable, "train_model.py"], 
                              capture_output=True, text=True, check=True)
        print("✅ Model training completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Model training failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def start_api():
    """Start the API server"""
    print("🚀 Starting API server...")
    print("📍 API will be available at: http://localhost:8000")
    print("📖 Interactive docs at: http://localhost:8000/docs")
    print("🛑 Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        subprocess.run([sys.executable, "app.py"], check=True)
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to start API server: {e}")

def main():
    """Main startup function"""
    print("🚀 ML Classification API Startup")
    print("=" * 40)
    
    # Check environment
    if not check_environment():
        sys.exit(1)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Check if model exists, train if not
    if not check_model():
        print("🔄 Training model...")
        if not train_model():
            print("❌ Failed to train model. Exiting.")
            sys.exit(1)
    
    # Start API
    start_api()

if __name__ == "__main__":
    main()
