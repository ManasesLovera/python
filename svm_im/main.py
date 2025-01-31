from fastapi import FastAPI
import pytesseract
from PIL import Image

# Load the image
image = Image.open("")

app = FastAPI()

@app.get("/")
async def read_root():
    return { "message": "Hello World!" }