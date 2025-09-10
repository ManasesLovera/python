# ML Classification API - API Guide

Complete guide to using the ML Classification API for ARS Primera document classification.

## API Overview

The ML Classification API provides RESTful endpoints for text classification using machine learning models. It supports multiple model types and provides real-time classification with confidence scores.

**Base URL**: `http://localhost:8000/api/v1`
**Documentation**: `http://localhost:8000/docs` (Swagger UI)

## Authentication

Currently, no authentication is required. For production deployment, add authentication middleware.

## Endpoints

### 1. Classify Text

Classify a text document using the specified model.

**Endpoint**: `POST /api/v1/classify`

**Request Body**:
```json
{
    "text": "Your text to classify",
    "model_type": "svm"
}
```

**Parameters**:
- `text` (string, required): Text to classify (1-10,000 characters)
- `model_type` (string, optional): Model type to use (default: "svm")

**Response**:
```json
{
    "tagClass": "Indicación Médica de Estudios",
    "score": 0.95,
    "model_used": "svm",
    "processing_time_ms": 15.2
}
```

**Response Fields**:
- `tagClass`: Predicted document class
- `score`: Confidence score (0.0 to 1.0)
- `model_used`: Model type used for prediction
- `processing_time_ms`: Processing time in milliseconds

**Example cURL**:
```bash
curl -X POST "http://localhost:8000/api/v1/classify" \
     -H "Content-Type: application/json" \
     -d '{
       "text": "Paciente: Cédula o Pasaporte: Edad: Teléfono: Ars: DETERMINACIÓN Centro Oriental de Ginecología Obstetricia y Especialidades",
       "model_type": "svm"
     }'
```

**Example Python**:
```python
import requests

response = requests.post("http://localhost:8000/api/v1/classify", json={
    "text": "Your text here",
    "model_type": "svm"
})

result = response.json()
print(f"Class: {result['tagClass']}")
print(f"Score: {result['score']}")
```

### 2. Train Model

Train a new model or retrain an existing one.

**Endpoint**: `POST /api/v1/train`

**Request Body**:
```json
{
    "model_type": "svm",
    "retrain": false
}
```

**Parameters**:
- `model_type` (string, required): Type of model to train
- `retrain` (boolean, optional): Whether to retrain existing model (default: false)

**Response**:
```json
{
    "model_type": "svm",
    "success": true,
    "message": "Model trained and saved successfully",
    "metadata": {
        "model_name": "svm",
        "training_samples": 885,
        "num_classes": 7,
        "classes": ["Historia Clínica", "Indicación Médica de Estudios", ...],
        "accuracy": 0.998
    }
}
```

**Example cURL**:
```bash
curl -X POST "http://localhost:8000/api/v1/train" \
     -H "Content-Type: application/json" \
     -d '{
       "model_type": "svm",
       "retrain": true
     }'
```

### 3. Get Available Models

Get information about all available models.

**Endpoint**: `GET /api/v1/models`

**Response**:
```json
[
    {
        "model_type": "svm",
        "is_available": true,
        "is_loaded": false,
        "metadata": {
            "model_name": "svm",
            "training_samples": 885,
            "num_classes": 7,
            "classes": ["Historia Clínica", "Indicación Médica de Estudios", ...],
            "accuracy": 0.998
        }
    }
]
```

**Example cURL**:
```bash
curl -X GET "http://localhost:8000/api/v1/models"
```

### 4. Get Model Information

Get detailed information about a specific model.

**Endpoint**: `GET /api/v1/models/{model_type}`

**Parameters**:
- `model_type` (string, path): Type of model to get info for

**Response**:
```json
{
    "model_type": "svm",
    "is_available": true,
    "is_loaded": true,
    "metadata": {
        "model_name": "svm",
        "training_samples": 885,
        "num_classes": 7,
        "classes": ["Historia Clínica", "Indicación Médica de Estudios", ...],
        "accuracy": 0.998
    }
}
```

**Example cURL**:
```bash
curl -X GET "http://localhost:8000/api/v1/models/svm"
```

### 5. Delete Model

Delete a trained model.

**Endpoint**: `DELETE /api/v1/models/{model_type}`

**Parameters**:
- `model_type` (string, path): Type of model to delete

**Response**:
```json
{
    "message": "Model 'svm' deleted successfully"
}
```

**Example cURL**:
```bash
curl -X DELETE "http://localhost:8000/api/v1/models/svm"
```

### 6. Health Check

Check API health and status.

**Endpoint**: `GET /api/v1/health`

**Response**:
```json
{
    "status": "healthy",
    "available_models": ["svm"],
    "total_loaded_models": 1
}
```

**Example cURL**:
```bash
curl -X GET "http://localhost:8000/api/v1/health"
```

## Error Handling

### Error Response Format

```json
{
    "error": "Error message",
    "detail": "Detailed error information",
    "status_code": 400
}
```

### Common Error Codes

- **400 Bad Request**: Invalid request data
- **404 Not Found**: Model or endpoint not found
- **422 Unprocessable Entity**: Validation error
- **500 Internal Server Error**: Server error

### Example Error Responses

**Model Not Found**:
```json
{
    "error": "Model 'invalid_model' not found",
    "detail": "Available models: ['svm']",
    "status_code": 404
}
```

**Validation Error**:
```json
{
    "error": "Validation error",
    "detail": "1 validation error for ClassificationRequest\ntext\n  String should have at most 10000 characters [type=string_too_long, input_value='Very long text...', input_type=str]",
    "status_code": 422
}
```

## Supported Document Classes

The API can classify documents into the following classes:

1. **Indicación Médica de Estudios** - Medical study indications
2. **Historia Clínica** - Clinical history
3. **Resultados de Laboratorio** - Laboratory results
4. **Informe de Tomografía** - CT scan reports
5. **Informe de Sonografía** - Ultrasound reports
6. **Informe de Radiografía** - X-ray reports
7. **Informe de Resonancia Magnética** - MRI reports

## Rate Limiting

Currently, no rate limiting is implemented. For production deployment, consider adding rate limiting middleware.

## Performance

- **Average Response Time**: 2-5ms
- **Throughput**: ~1000 requests/second
- **Memory Usage**: ~100MB (with loaded models)

## Testing

### Using the Test Script

```bash
python test_api.py
```

### Manual Testing

1. **Start the API**:
   ```bash
   python app.py
   ```

2. **Open Swagger UI**: http://localhost:8000/docs

3. **Test endpoints** using the interactive interface

### Load Testing

```bash
# Install Apache Bench
# Test with 100 requests, 10 concurrent
ab -n 100 -c 10 -H "Content-Type: application/json" \
   -p test_data.json http://localhost:8000/api/v1/classify
```

## Integration Examples

### JavaScript/Node.js

```javascript
const axios = require('axios');

async function classifyText(text) {
    try {
        const response = await axios.post('http://localhost:8000/api/v1/classify', {
            text: text,
            model_type: 'svm'
        });
        return response.data;
    } catch (error) {
        console.error('Classification failed:', error.response.data);
    }
}

// Usage
classifyText('Your text here').then(result => {
    console.log('Class:', result.tagClass);
    console.log('Score:', result.score);
});
```

### Python

```python
import requests
import json

def classify_text(text, model_type='svm'):
    url = 'http://localhost:8000/api/v1/classify'
    payload = {
        'text': text,
        'model_type': model_type
    }
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f'Error: {e}')
        return None

# Usage
result = classify_text('Your text here')
if result:
    print(f"Class: {result['tagClass']}")
    print(f"Score: {result['score']}")
```

### cURL

```bash
# Classify text
curl -X POST "http://localhost:8000/api/v1/classify" \
     -H "Content-Type: application/json" \
     -d '{"text": "Your text here", "model_type": "svm"}'

# Get models
curl -X GET "http://localhost:8000/api/v1/models"

# Health check
curl -X GET "http://localhost:8000/api/v1/health"
```

## Monitoring and Logging

- **Logs**: Check `logs/api.log` for detailed logs
- **Health**: Use `/api/v1/health` endpoint for monitoring
- **Metrics**: Response times and success rates in logs

## Production Considerations

1. **Authentication**: Add API key or JWT authentication
2. **Rate Limiting**: Implement request rate limiting
3. **CORS**: Configure proper CORS settings
4. **HTTPS**: Use SSL/TLS in production
5. **Load Balancing**: Use multiple API instances
6. **Monitoring**: Add application performance monitoring
7. **Backup**: Regular model and data backups
