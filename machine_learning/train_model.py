"""
Script to train and save the SVM model
"""
import sys
from pathlib import Path

# Add the current directory to Python path
sys.path.append(str(Path(__file__).parent))

from models.model_factory import ModelFactory
from data.dataset_loader import DatasetLoader
from persistence.model_manager import ModelManager
from config import DATASET_PATH, MODEL_CONFIGS
from utils.logger import setup_logger

logger = setup_logger()


def train_svm_model():
    """Train and save the SVM model"""
    try:
        logger.info("Starting SVM model training...")
        
        # Load dataset
        logger.info("Loading dataset...")
        dataset_loader = DatasetLoader(str(DATASET_PATH))
        X, y = dataset_loader.get_training_data()  # Use same train/test split as original
        
        logger.info(f"Dataset loaded: {len(X)} samples")
        logger.info(f"Classes: {set(y)}")
        
        # Create SVM classifier
        logger.info("Creating SVM classifier...")
        classifier = ModelFactory.create_classifier("svm")
        
        # Get SVM configuration
        svm_config = MODEL_CONFIGS["svm"]
        vectorizer_params = svm_config.get("vectorizer_params", {})
        
        # Train the model
        logger.info("Training model...")
        metadata = classifier.train(X, y, vectorizer_params)
        
        logger.info(f"Training completed. Accuracy: {metadata['accuracy']:.3f}")
        logger.info(f"Classes: {metadata['classes']}")
        
        # Save the model
        logger.info("Saving model...")
        model_manager = ModelManager()
        model_path = model_manager.save_model(classifier, "svm")
        
        logger.info(f"Model saved successfully to: {model_path}")
        logger.info("Training completed successfully!")
        
        return True
        
    except Exception as e:
        logger.error(f"Training failed: {str(e)}")
        return False


if __name__ == "__main__":
    success = train_svm_model()
    sys.exit(0 if success else 1)
