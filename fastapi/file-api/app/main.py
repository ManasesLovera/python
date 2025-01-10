from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse # type: ignore
from fastapi.middleware.cors import CORSMiddleware # type: ignore
import os
import mimetypes

app = FastAPI()

# Configure CORS (Cross-Origin Resource Sharing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow requests from any origin (frontend, localhost, etc.)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, PUT, DELETE)
    allow_headers=["*"],  # Allow all headers
)

# Directory where PDFs are stored
PDF_DIR = os.path.join(os.path.dirname(__file__), "static")

@app.get("/")
def root():
    return {"message": "Welcome to the FastAPI PDF Service!"}

# Endpoint to VIEW the PDF (inline)
@app.get("/file/view/{filename}")
def view_file(filename: str):
    file_path = os.path.join(PDF_DIR, filename)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    # Detect the MIME type dynamically
    media_type, _ = mimetypes.guess_type(file_path)
    if not media_type:
        media_type = "application/octet-stream"  # Fallback for unknown file types

    return FileResponse(file_path, media_type=media_type)
    
# Endpoint to DOWNLOAD the PDF
@app.get("/file/download/{filename}")
def download_file(filename: str):
    file_path = os.path.join(PDF_DIR, filename)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    # Detect the MIME type dynamically
    media_type, _ = mimetypes.guess_type(file_path)
    if not media_type:
        media_type = "application/octet-stream"  # Fallback for unknown file types

    return FileResponse(
        file_path,
        media_type=media_type,
        filename=filename,
        headers={
            "Content-Disposition": f"attachment; filename={filename}"
        }
    )