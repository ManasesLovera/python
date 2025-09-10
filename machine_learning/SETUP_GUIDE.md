# ML Classification API - Setup Guide

This guide will help you set up and run the ML Classification API for ARS Primera document classification.

## Prerequisites

- **Python 3.11+** (recommended)
- **Conda** or **Miniconda** (recommended)
- **Git** (for cloning the repository)

## Quick Start (Conda - Recommended)

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd ml-classification-api
```

### 2. Create Conda Environment
```bash
# Create environment from file
conda env create -f environment.yml

# Activate environment
conda activate ml-classification-api
```

### 3. Train the Model
```bash
python train_model.py
```

### 4. Start the API Server
```bash
python app.py
```

### 5. Access the API
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/api/v1/health
- **API Base URL**: http://localhost:8000/api/v1

## Alternative Setup (pip)

### 1. Create Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Linux/Mac)
source venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Train and Run
```bash
python train_model.py
python app.py
```

## Project Structure

```
ml_classification_api/
├── app.py                     # Main FastAPI application
├── config.py                  # Configuration settings
├── environment.yml            # Conda environment file
├── requirements.txt           # pip requirements
├── train_model.py             # Model training script
├── test_api.py                # API testing script
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

## Configuration

Edit `config.py` to customize:
- Model parameters
- API settings
- File paths
- Logging levels

## Troubleshooting

### Common Issues

1. **Port Already in Use**
   ```bash
   # Kill process using port 8000
   netstat -ano | findstr :8000
   taskkill /PID <PID> /F
   ```

2. **Model Not Found**
   ```bash
   # Retrain the model
   python train_model.py
   ```

3. **Permission Errors**
   ```bash
   # Run as administrator (Windows)
   # Or check file permissions
   ```

4. **Dependencies Issues**
   ```bash
   # Update conda
   conda update conda
   
   # Recreate environment
   conda env remove -n ml-classification-api
   conda env create -f environment.yml
   ```

## Development

### Adding New Models

1. Create new classifier in `models/`
2. Register in `models/model_factory.py`
3. Add configuration in `config.py`
4. Test with `python test_api.py`

### Running Tests

```bash
# Test API endpoints
python test_api.py

# Test specific functionality
python -m pytest tests/
```

## Production Deployment

### Using Gunicorn
```bash
pip install gunicorn
gunicorn app:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Using Docker
```dockerfile
FROM python:3.11-slim
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["python", "app.py"]
```

## Environment Variables

Create `.env` file for production:
```env
API_HOST=0.0.0.0
API_PORT=8000
LOG_LEVEL=INFO
MODELS_DIR=./saved_models
```

## Support

For issues and questions:
1. Check the logs in `logs/` directory
2. Review the API documentation at `/docs`
3. Test with `python test_api.py`
