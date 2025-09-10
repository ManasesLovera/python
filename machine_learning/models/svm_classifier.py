"""
SVM Classifier implementation
"""
import joblib
import json
from pathlib import Path
from typing import Dict, Any
from sklearn.linear_model import SGDClassifier
from .base_classifier import BaseClassifier


class SVMClassifier(BaseClassifier):
    """
    SVM Classifier using SGDClassifier with hinge loss
    """
    
    def __init__(self):
        super().__init__("svm")
    
    def _create_model(self, **params) -> SGDClassifier:
        """Create SGDClassifier with SVM parameters"""
        return SGDClassifier(**params)
    
    def _get_model_params(self) -> Dict[str, Any]:
        """Get SVM-specific parameters"""
        return {
            "loss": "hinge",
            "class_weight": "balanced",
            "random_state": 42
        }
    
    def save_model(self, path: str) -> None:
        """
        Save the trained SVM model and vectorizer to disk
        
        Args:
            path: Directory path to save the model
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before saving")
        
        path = Path(path)
        path.mkdir(parents=True, exist_ok=True)
        
        # Save model
        model_path = path / "model.pkl"
        joblib.dump(self.model, model_path, compress=True)
        
        # Save vectorizer
        vectorizer_path = path / "vectorizer.pkl"
        joblib.dump(self.vectorizer, vectorizer_path, compress=True)
        
        # Save metadata
        metadata_path = path / "metadata.json"
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(self.metadata, f, indent=2, ensure_ascii=False)
        
        print(f"Model saved to {path}")
    
    def load_model(self, path: str) -> None:
        """
        Load a trained SVM model and vectorizer from disk
        
        Args:
            path: Directory path where the model is saved
        """
        path = Path(path)
        
        # Load model
        model_path = path / "model.pkl"
        if not model_path.exists():
            raise FileNotFoundError(f"Model file not found: {model_path}")
        self.model = joblib.load(model_path)
        
        # Load vectorizer
        vectorizer_path = path / "vectorizer.pkl"
        if not vectorizer_path.exists():
            raise FileNotFoundError(f"Vectorizer file not found: {vectorizer_path}")
        self.vectorizer = joblib.load(vectorizer_path)
        
        # Load metadata
        metadata_path = path / "metadata.json"
        if metadata_path.exists():
            with open(metadata_path, 'r', encoding='utf-8') as f:
                self.metadata = json.load(f)
        
        # Set classes and training status
        self.classes_ = self.model.classes_
        self.is_trained = True
        
        print(f"Model loaded from {path}")
