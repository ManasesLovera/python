"""
API endpoints for ML Classification API
"""
import time
from typing import List
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse

from .schemas import (
    ClassificationRequest, 
    ClassificationResponse, 
    ModelInfo, 
    TrainingRequest, 
    TrainingResponse,
    ErrorResponse
)
from persistence.model_manager import ModelManager
from models.model_factory import ModelFactory
from data.dataset_loader import DatasetLoader
from config import DATASET_PATH, MODEL_CONFIGS

router = APIRouter()

# Global model manager instance
model_manager = ModelManager()


@router.post("/classify", response_model=ClassificationResponse)
async def classify_text(request: ClassificationRequest):
    """
    Classify a text using the specified model
    """
    try:
        # Check if model is available
        if not model_manager.is_model_available(request.model_type):
            raise HTTPException(
                status_code=404, 
                detail=f"Model '{request.model_type}' not found. Available models: {model_manager.get_available_models()}"
            )
        
        # Load model
        classifier = model_manager.load_model(request.model_type)
        
        # Measure processing time
        start_time = time.time()
        
        # Make prediction
        result = classifier.predict(request.text)
        
        processing_time = (time.time() - start_time) * 1000  # Convert to milliseconds
        
        return ClassificationResponse(
            tagClass=result["tagClass"],
            score=result["score"],
            model_used=result["model_used"],
            processing_time_ms=round(processing_time, 2)
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Classification failed: {str(e)}")


@router.post("/train", response_model=TrainingResponse)
async def train_model(request: TrainingRequest):
    """
    Train a new model or retrain an existing one
    """
    try:
        # Check if model type is supported
        if request.model_type not in MODEL_CONFIGS:
            available_models = list(MODEL_CONFIGS.keys())
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported model type: {request.model_type}. Available: {available_models}"
            )
        
        # Check if model already exists and retrain is not requested
        if model_manager.is_model_available(request.model_type) and not request.retrain:
            raise HTTPException(
                status_code=400,
                detail=f"Model '{request.model_type}' already exists. Use retrain=true to retrain."
            )
        
        # Load dataset
        dataset_loader = DatasetLoader(str(DATASET_PATH))
        X, y = dataset_loader.get_training_data()  # Use same train/test split as original
        
        # Create and train classifier
        classifier = ModelFactory.create_classifier(request.model_type)
        
        # Get model configuration
        model_config = MODEL_CONFIGS[request.model_type]
        vectorizer_params = model_config.get("vectorizer_params", {})
        
        # Train the model
        metadata = classifier.train(X, y, vectorizer_params)
        
        # Save the trained model
        model_path = model_manager.save_model(classifier, request.model_type)
        
        return TrainingResponse(
            model_type=request.model_type,
            success=True,
            message=f"Model trained and saved successfully to {model_path}",
            metadata=metadata
        )
        
    except Exception as e:
        return TrainingResponse(
            model_type=request.model_type,
            success=False,
            message=f"Training failed: {str(e)}",
            metadata=None
        )


@router.get("/models", response_model=List[ModelInfo])
async def get_models():
    """
    Get information about all available models
    """
    try:
        available_models = model_manager.get_available_models()
        model_info_list = []
        
        for model_type in available_models:
            try:
                metadata = model_manager.get_model_info(model_type)
                is_loaded = model_type in model_manager._loaded_models
                
                model_info_list.append(ModelInfo(
                    model_type=model_type,
                    is_available=True,
                    is_loaded=is_loaded,
                    metadata=metadata
                ))
            except Exception as e:
                model_info_list.append(ModelInfo(
                    model_type=model_type,
                    is_available=True,
                    is_loaded=False,
                    metadata={"error": str(e)}
                ))
        
        return model_info_list
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get models: {str(e)}")


@router.get("/models/{model_type}", response_model=ModelInfo)
async def get_model_info(model_type: str):
    """
    Get detailed information about a specific model
    """
    try:
        if not model_manager.is_model_available(model_type):
            raise HTTPException(
                status_code=404,
                detail=f"Model '{model_type}' not found"
            )
        
        metadata = model_manager.get_model_info(model_type)
        is_loaded = model_type in model_manager._loaded_models
        
        return ModelInfo(
            model_type=model_type,
            is_available=True,
            is_loaded=is_loaded,
            metadata=metadata
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get model info: {str(e)}")


@router.delete("/models/{model_type}")
async def delete_model(model_type: str):
    """
    Delete a trained model
    """
    try:
        if not model_manager.is_model_available(model_type):
            raise HTTPException(
                status_code=404,
                detail=f"Model '{model_type}' not found"
            )
        
        success = model_manager.delete_model(model_type)
        
        if success:
            return {"message": f"Model '{model_type}' deleted successfully"}
        else:
            raise HTTPException(status_code=500, detail="Failed to delete model")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete model: {str(e)}")


@router.get("/health")
async def health_check():
    """
    Health check endpoint
    """
    return {
        "status": "healthy",
        "available_models": model_manager.get_available_models(),
        "total_loaded_models": len(model_manager._loaded_models)
    }
