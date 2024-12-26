# FastAPI PDF API 🚀  

This project allows users to access and download PDF files through specific endpoints. The API leverages FastAPI and Uvicorn for fast and efficient file serving. 

## Description  
This project allows users to access and download PDF files through a specific endpoint. The API leverages FastAPI and Uvicorn for fast and efficient file serving.  

---
## Requirements  
- Python 3.8+  
- Git  
---

## Technologies  
- **FastAPI** – A modern, high-performance web framework for building APIs with Python.  
- **Uvicorn** – A lightweight and fast ASGI server to run FastAPI applications asynchronously.  

---

## Installation and Setup  

### 1. Clone the Project  
```bash
git clone https://github.com/your-username/fastapi-pdf-api.git
cd fastapi-pdf-api
```
### 2. Create and Activate a Virtual Environment
- **Windows**:
```bash
Copy code
python -m venv venv
venv\Scripts\activate
```
- **Linux/Mac**:
```bash
Copy code
python -m venv venv
source venv/bin/activate
```
### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

## Running the Project
1. From the project root, run:
```bash
uvicorn app.main:app --reload
```
2. Access the API:
- Interactive documentation (Swagger): `http://127.0.0.1:8000/docs`.

## Project Structure
```
fastapi-pdf-api/
│
├── app/
│   ├── main.py        # Main API code
│   └── static/        # Folder for storing PDF files
│       └── example.pdf
│
├── venv/              # Virtual environment (ignored by git)
├── requirements.txt   # List of dependencies
└── README.md          # Project documentation
```

## Adding PDFs
1. Place your PDF files in the `app/static/` folder.
2. Access the files through the endpoint: `GET /pdf/{pdf_filename}`.
- Example: `http://127.0.0.1:8000/pdf/example.pdf`.

## Endpoints

1. View PDF in Browser
    - Endpoint: `GET /pdf/view/{filename}`
    - Description: Displays the PDF directly in the browser.
    - Example: `curl http://127.0.0.1:8000/pdf/view/example.pdf`

2. Download PDF
    - Endpoint: `GET /pdf/download/{filename}`
    - Description: Forces the download of the PDF file.
    - Example: `curl -O http://127.0.0.1:8000/pdf/download/example.pdf`

## Notes:
- Ensure that PDF files are placed in the app/static/ directory.
- The API validates the existence of the file. If the file is not found, it returns a 404 error.
- This API does not include authentication by default. Add authentication if exposing the API publicly.
- Only .pdf files are supported.