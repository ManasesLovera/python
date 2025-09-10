# ML Classification API

A scalable FastAPI-based machine learning classification API that supports multiple models for text classification. Currently implements SVM classifier for ARS Primera document classification.

## 📚 Documentation

- **[Setup Guide](SETUP_GUIDE.md)** - Complete setup and installation instructions
- **[API Guide](API_GUIDE.md)** - Comprehensive API documentation and usage examples
- **[Swagger UI](http://localhost:8000/docs)** - Interactive API documentation (when running)

## ✨ Features

- **Multi-model support**: Easy to add new classification models
- **Model persistence**: Save and load trained models using joblib
- **RESTful API**: Clean FastAPI-based endpoints
- **Interactive Documentation**: Swagger UI at `/docs`
- **Health monitoring**: Health check and model status endpoints
- **Error handling**: Comprehensive error handling and validation
- **Conda Support**: Easy environment setup with conda

## Architecture

```
ml_classification_api/
├── app.py                     # Main FastAPI application
├── config.py                  # Configuration settings
├── requirements.txt           # Dependencies
├── models/                    # Model implementations
│   ├── base_classifier.py    # Abstract base class
│   ├── svm_classifier.py     # SVM implementation
│   └── model_factory.py      # Model factory
├── data/                      # Data management
│   ├── dataset_loader.py     # Dataset utilities
│   └── dataset.json          # Training data
├── persistence/               # Model persistence
│   └── model_manager.py      # Save/load models
├── api/                      # API layer
│   ├── endpoints.py          # API endpoints
│   └── schemas.py            # Request/response models
├── utils/                     # Utilities
│   └── logger.py             # Logging configuration
└── saved_models/              # Persisted models
    └── svm/                  # SVM model files
```

## 🚀 Quick Start

### Option 1: Automated Setup (Easiest)
```bash
# Windows
start_api.bat

# Linux/Mac
./start_api.sh

# Or use Python directly
python start_api.py
```

### Option 2: Manual Setup

#### Conda (Recommended)
```bash
# Create and activate environment
conda env create -f environment.yml
conda activate ml-classification-api

# Train model and start API
python train_model.py
python app.py
```

#### pip
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Train model and start API
python train_model.py
python app.py
```

**Access the API**: http://localhost:8000
**Interactive Docs**: http://localhost:8000/docs

> 📖 For detailed setup instructions, see [Setup Guide](SETUP_GUIDE.md)

## 🔗 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/v1/classify` | Classify text with specified model |
| `POST` | `/api/v1/train` | Train new or retrain existing model |
| `GET` | `/api/v1/models` | List all available models |
| `GET` | `/api/v1/models/{type}` | Get specific model information |
| `DELETE` | `/api/v1/models/{type}` | Delete a trained model |
| `GET` | `/api/v1/health` | Health check and status |

### Example: Classify Text
```bash
curl -X POST "http://localhost:8000/api/v1/classify" \
     -H "Content-Type: application/json" \
     -d '{"text": "Your text here", "model_type": "svm"}'
```

**Response**:
```json
{
    "tagClass": "Resultados de Laboratorio",
    "score": 0.95,
    "model_used": "svm",
    "processing_time_ms": 15.2
}
```

> 📖 For complete API documentation, see [API Guide](API_GUIDE.md)

## Usage Examples

### Python
```python
import requests

# Classify text
response = requests.post("http://localhost:8000/api/v1/classify", json={
    "text": "Paciente: Cédula o Pasaporte...",
    "model_type": "svm"
})

result = response.json()
print(f"Class: {result['tagClass']}")
print(f"Score: {result['score']}")
```

### cURL
```bash
curl -X POST "http://localhost:8000/api/v1/classify" \
     -H "Content-Type: application/json" \
     -d '{"text": "Your text here", "model_type": "svm"}'
```

## Testing

Run the test script to verify everything works:

```bash
python test_api.py
```

## Adding New Models

1. **Create a new classifier class** in `models/`:
   ```python
   class DecisionTreeClassifier(BaseClassifier):
       def _create_model(self, **params):
           return DecisionTreeClassifier(**params)
       
       def _get_model_params(self):
           return {"max_depth": 10, "random_state": 42}
   ```

2. **Register it in the factory** (`models/model_factory.py`):
   ```python
   _models = {
       "svm": SVMClassifier,
       "decision_tree": DecisionTreeClassifier,  # Add here
   }
   ```

3. **Add configuration** in `config.py`:
   ```python
   MODEL_CONFIGS = {
       "svm": {...},
       "decision_tree": {  # Add here
           "class": "DecisionTreeClassifier",
           "params": {...}
       }
   }
   ```

## Model Persistence

Models are saved using joblib in the `saved_models/` directory:
- `model.pkl`: Trained sklearn model
- `vectorizer.pkl`: Fitted TF-IDF vectorizer
- `metadata.json`: Model metadata and training info

## Configuration

Edit `config.py` to customize:
- Model parameters
- API settings
- File paths
- Logging levels

## Production Deployment

For production deployment:
1. Set proper CORS origins in `app.py`
2. Use a production WSGI server (e.g., Gunicorn)
3. Add authentication/authorization
4. Set up monitoring and logging
5. Use environment variables for configuration

## License

MIT License
