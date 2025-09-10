"""
Model factory for creating different types of classifiers
"""
from typing import Dict, Type
from .base_classifier import BaseClassifier
from .svm_classifier import SVMClassifier


class ModelFactory:
    """
    Factory class for creating different types of classifiers
    """
    
    _models: Dict[str, Type[BaseClassifier]] = {
        "svm": SVMClassifier,
        # Add more models here as they are implemented
        # "decision_tree": DecisionTreeClassifier,
        # "random_forest": RandomForestClassifier,
    }
    
    @classmethod
    def create_classifier(cls, model_type: str) -> BaseClassifier:
        """
        Create a classifier instance based on the model type
        
        Args:
            model_type: Type of classifier to create (e.g., 'svm', 'decision_tree')
            
        Returns:
            Instance of the requested classifier
            
        Raises:
            ValueError: If the model type is not supported
        """
        if model_type not in cls._models:
            available_models = list(cls._models.keys())
            raise ValueError(
                f"Unsupported model type: {model_type}. "
                f"Available models: {available_models}"
            )
        
        return cls._models[model_type]()
    
    @classmethod
    def get_available_models(cls) -> list:
        """
        Get list of available model types
        
        Returns:
            List of available model type names
        """
        return list(cls._models.keys())
    
    @classmethod
    def register_model(cls, model_type: str, model_class: Type[BaseClassifier]) -> None:
        """
        Register a new model type
        
        Args:
            model_type: Name of the model type
            model_class: Class that implements BaseClassifier
        """
        cls._models[model_type] = model_class
