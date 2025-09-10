"""
API package for ML Classification API
"""
from .endpoints import router
from .schemas import ClassificationRequest, ClassificationResponse, ModelInfo

__all__ = ["router", "ClassificationRequest", "ClassificationResponse", "ModelInfo"]
