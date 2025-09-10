"""
Configuration settings for the ML Classification API
"""
import os
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
MODELS_DIR = BASE_DIR / "saved_models"
LOGS_DIR = BASE_DIR / "logs"

# Create directories if they don't exist
for directory in [DATA_DIR, MODELS_DIR, LOGS_DIR]:
    directory.mkdir(exist_ok=True)

# Dataset configuration
DATASET_PATH = DATA_DIR / "dataset.json"

# Model configurations
MODEL_CONFIGS = {
    "svm": {
        "class": "SVMClassifier",
        "params": {
            "loss": "hinge",
            "class_weight": "balanced",
            "random_state": 42
        },
        "vectorizer_params": {
            "ngram_range": (1, 2),
            "min_df": 2,
            "max_df": 0.9
        }
    },
    "decision_tree": {
        "class": "DecisionTreeClassifier",
        "params": {
            "max_depth": 10,
            "random_state": 42,
            "class_weight": "balanced"
        },
        "vectorizer_params": {
            "ngram_range": (1, 2),
            "min_df": 2,
            "max_df": 0.9
        }
    }
}

# API configuration
API_CONFIG = {
    "title": "ML Classification API",
    "description": "Multi-model text classification API for ARS Primera documents",
    "version": "1.0.0",
    "host": "0.0.0.0",
    "port": 8000
}

# Model persistence settings
PERSISTENCE_CONFIG = {
    "format": "joblib",  # or "pickle"
    "compress": True,
    "include_metadata": True
}
