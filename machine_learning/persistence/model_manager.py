"""
Model management utilities for saving and loading models
"""
import os
from pathlib import Path
from typing import Dict, List, Optional
from models.base_classifier import BaseClassifier
from models.model_factory import ModelFactory
from config import MODELS_DIR


class ModelManager:
    """
    Manages model persistence and loading
    """
    
    def __init__(self, models_dir: str = None):
        """
        Initialize the model manager
        
        Args:
            models_dir: Directory to store models (defaults to config)
        """
        self.models_dir = Path(models_dir or MODELS_DIR)
        self.models_dir.mkdir(exist_ok=True)
        self._loaded_models: Dict[str, BaseClassifier] = {}
    
    def save_model(self, classifier: BaseClassifier, model_type: str) -> str:
        """
        Save a trained classifier
        
        Args:
            classifier: Trained classifier instance
            model_type: Type of the model (e.g., 'svm')
            
        Returns:
            Path where the model was saved
        """
        if not classifier.is_trained:
            raise ValueError("Cannot save untrained model")
        
        model_path = self.models_dir / model_type
        classifier.save_model(str(model_path))
        
        return str(model_path)
    
    def load_model(self, model_type: str, force_reload: bool = False) -> BaseClassifier:
        """
        Load a trained model
        
        Args:
            model_type: Type of model to load (e.g., 'svm')
            force_reload: Force reload even if already in memory
            
        Returns:
            Loaded classifier instance
        """
        if not force_reload and model_type in self._loaded_models:
            return self._loaded_models[model_type]
        
        # Create new classifier instance
        classifier = ModelFactory.create_classifier(model_type)
        
        # Load the trained model
        model_path = self.models_dir / model_type
        if not model_path.exists():
            raise FileNotFoundError(f"No saved model found for type: {model_type}")
        
        classifier.load_model(str(model_path))
        
        # Cache the loaded model
        self._loaded_models[model_type] = classifier
        
        return classifier
    
    def get_available_models(self) -> List[str]:
        """
        Get list of available saved models
        
        Returns:
            List of model types that have been saved
        """
        available = []
        for item in self.models_dir.iterdir():
            if item.is_dir() and (item / "model.pkl").exists():
                available.append(item.name)
        return available
    
    def get_model_info(self, model_type: str) -> Dict:
        """
        Get information about a saved model
        
        Args:
            model_type: Type of model to get info for
            
        Returns:
            Dictionary with model information
        """
        model_path = self.models_dir / model_type
        metadata_path = model_path / "metadata.json"
        
        if not metadata_path.exists():
            raise FileNotFoundError(f"No metadata found for model: {model_type}")
        
        import json
        with open(metadata_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def delete_model(self, model_type: str) -> bool:
        """
        Delete a saved model
        
        Args:
            model_type: Type of model to delete
            
        Returns:
            True if deleted successfully, False otherwise
        """
        model_path = self.models_dir / model_type
        
        if not model_path.exists():
            return False
        
        import shutil
        shutil.rmtree(model_path)
        
        # Remove from cache if loaded
        if model_type in self._loaded_models:
            del self._loaded_models[model_type]
        
        return True
    
    def is_model_available(self, model_type: str) -> bool:
        """
        Check if a model is available
        
        Args:
            model_type: Type of model to check
            
        Returns:
            True if model is available, False otherwise
        """
        model_path = self.models_dir / model_type
        return model_path.exists() and (model_path / "model.pkl").exists()
