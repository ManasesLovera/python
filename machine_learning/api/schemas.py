"""
Pydantic schemas for API request/response models
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Dict, Any, Optional


class ClassificationRequest(BaseModel):
    """Request schema for text classification"""
    model_config = ConfigDict(protected_namespaces=())
    
    text: str = Field(..., description="Text to classify", min_length=1, max_length=10000)
    model_type: str = Field(default="svm", description="Type of model to use for classification")


class ClassificationResponse(BaseModel):
    """Response schema for text classification"""
    model_config = ConfigDict(protected_namespaces=())
    
    tagClass: str = Field(..., description="Predicted class")
    score: float = Field(..., description="Confidence score", ge=0.0, le=1.0)
    model_used: str = Field(..., description="Model type used for prediction")
    processing_time_ms: Optional[float] = Field(None, description="Processing time in milliseconds")


class ModelInfo(BaseModel):
    """Schema for model information"""
    model_config = ConfigDict(protected_namespaces=())
    
    model_type: str = Field(..., description="Type of model")
    is_available: bool = Field(..., description="Whether model is available")
    is_loaded: bool = Field(..., description="Whether model is loaded in memory")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Model metadata")


class TrainingRequest(BaseModel):
    """Request schema for model training"""
    model_config = ConfigDict(protected_namespaces=())
    
    model_type: str = Field(..., description="Type of model to train")
    retrain: bool = Field(default=False, description="Whether to retrain existing model")


class TrainingResponse(BaseModel):
    """Response schema for model training"""
    model_config = ConfigDict(protected_namespaces=())
    
    model_type: str = Field(..., description="Type of model trained")
    success: bool = Field(..., description="Whether training was successful")
    message: str = Field(..., description="Training result message")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Training metadata")


class ErrorResponse(BaseModel):
    """Schema for error responses"""
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Detailed error information")
