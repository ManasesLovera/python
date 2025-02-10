import pytesseract
from PIL import Image

# Load the image
image = Image.open("")

# Extract text using pytesseract
text = pytesseract.image_to_string(image)

print("Extracted Text:")
print(text)