"""
Abstract base class for all classifiers
"""
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Tuple
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer


class BaseClassifier(ABC):
    """
    Abstract base class that defines the interface for all classifiers
    """
    
    def __init__(self, model_name: str):
        self.model_name = model_name
        self.model = None
        self.vectorizer = None
        self.classes_ = None
        self.is_trained = False
        self.metadata = {}
    
    @abstractmethod
    def _create_model(self, **params) -> Any:
        """Create the specific model instance"""
        pass
    
    @abstractmethod
    def _get_model_params(self) -> Dict[str, Any]:
        """Get model-specific parameters"""
        pass
    
    def train(self, X: List[str], y: List[str], vectorizer_params: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Train the classifier with the given data
        
        Args:
            X: List of text documents
            y: List of corresponding labels
            vectorizer_params: Parameters for TF-IDF vectorizer
            
        Returns:
            Dictionary with training results and metrics
        """
        # Create vectorizer
        vectorizer_params = vectorizer_params or {}
        self.vectorizer = TfidfVectorizer(**vectorizer_params)
        
        # Create model
        model_params = self._get_model_params()
        self.model = self._create_model(**model_params)
        
        # Transform text to features
        X_transformed = self.vectorizer.fit_transform(X)
        
        # Train model
        self.model.fit(X_transformed, y)
        
        # Store classes
        self.classes_ = self.model.classes_
        self.is_trained = True
        
        # Calculate training metrics
        y_pred = self.model.predict(X_transformed)
        accuracy = (y_pred == y).mean()
        
        self.metadata = {
            "model_name": self.model_name,
            "training_samples": len(X),
            "num_classes": len(self.classes_),
            "classes": self.classes_.tolist(),
            "accuracy": float(accuracy),
            "vectorizer_params": vectorizer_params,
            "model_params": model_params
        }
        
        return self.metadata
    
    def predict(self, text: str) -> Dict[str, Any]:
        """
        Predict the class and score for a single text
        
        Args:
            text: Input text to classify
            
        Returns:
            Dictionary with prediction results
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before making predictions")
        
        # Transform text
        text_transformed = self.vectorizer.transform([text])
        
        # Get prediction and score
        prediction = self.model.predict(text_transformed)[0]
        
        # Get prediction probabilities or decision function scores
        if hasattr(self.model, 'predict_proba'):
            scores = self.model.predict_proba(text_transformed)[0]
            max_score = float(max(scores))
        else:
            # For SVM, use decision function and normalize to [0,1]
            decision_scores = self.model.decision_function(text_transformed)[0]
            if len(decision_scores.shape) == 1:
                # Binary classification - normalize using sigmoid
                import numpy as np
                max_score = float(1 / (1 + np.exp(-decision_scores[0])))
            else:
                # Multi-class - normalize using softmax
                import numpy as np
                exp_scores = np.exp(decision_scores - np.max(decision_scores))
                softmax_scores = exp_scores / np.sum(exp_scores)
                max_score = float(max(softmax_scores))
        
        return {
            "tagClass": prediction,
            "score": max_score,
            "model_used": self.model_name
        }
    
    def predict_batch(self, texts: List[str]) -> List[Dict[str, Any]]:
        """
        Predict classes and scores for multiple texts
        
        Args:
            texts: List of input texts to classify
            
        Returns:
            List of dictionaries with prediction results
        """
        return [self.predict(text) for text in texts]
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the trained model"""
        return {
            "model_name": self.model_name,
            "is_trained": self.is_trained,
            "metadata": self.metadata
        }
    
    @abstractmethod
    def save_model(self, path: str) -> None:
        """Save the trained model to disk"""
        pass
    
    @abstractmethod
    def load_model(self, path: str) -> None:
        """Load a trained model from disk"""
        pass
