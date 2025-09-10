"""
Simple test script for the ML Classification API
"""
import requests
import json
import time

API_BASE_URL = "http://localhost:8000/api/v1"

def test_classification():
    """Test the classification endpoint"""
    print("Testing classification endpoint...")
    
    # Test data
    test_text = "Paciente: Cédula o Pasaporte: Edad: Teléfono: Ars: DETERMINACIÓN Centro Oriental de Ginecología Obstetricia y Especialidades"
    
    payload = {
        "text": test_text,
        "model_type": "svm"
    }
    
    try:
        response = requests.post(f"{API_BASE_URL}/classify", json=payload)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Classification successful!")
            print(f"Predicted class: {result['tagClass']}")
            print(f"Confidence score: {result['score']:.3f}")
            print(f"Model used: {result['model_used']}")
            print(f"Processing time: {result['processing_time_ms']}ms")
        else:
            print(f"❌ Classification failed: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")

def test_health():
    """Test the health endpoint"""
    print("\nTesting health endpoint...")
    
    try:
        response = requests.get(f"{API_BASE_URL}/health")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Health check successful!")
            print(f"Status: {result['status']}")
            print(f"Available models: {result['available_models']}")
            print(f"Loaded models: {result['total_loaded_models']}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")

def test_models():
    """Test the models endpoint"""
    print("\nTesting models endpoint...")
    
    try:
        response = requests.get(f"{API_BASE_URL}/models")
        
        if response.status_code == 200:
            models = response.json()
            print("✅ Models endpoint successful!")
            for model in models:
                print(f"Model: {model['model_type']}")
                print(f"  Available: {model['is_available']}")
                print(f"  Loaded: {model['is_loaded']}")
                if model['metadata']:
                    print(f"  Accuracy: {model['metadata'].get('accuracy', 'N/A')}")
        else:
            print(f"❌ Models endpoint failed: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    print("🚀 Starting API tests...")
    print("Make sure the API is running on http://localhost:8000")
    print("=" * 50)
    
    test_health()
    test_models()
    test_classification()
    
    print("\n" + "=" * 50)
    print("Tests completed!")
