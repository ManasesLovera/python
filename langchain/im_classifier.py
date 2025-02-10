### One-shot Classification with LLM (Langchain + OpenAI + OCR)
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage
import pytesseract
from PIL import Image
import os
from dotenv import load_dotenv # type: ignore

# Load environment variables from the .env file
load_dotenv()

llm = ChatOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    model_name="gpt-4", # Here I'm being explicit, but this is the default model used by ChatOpenAI at the time of writing.
)

# OCR function to Extract Text from Image
def extract_text_from_image(image_path):
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)
    return text

# Example prompt
prompt_template = """
Classify this text as 'Indicación Médical' or 'Other'.

All text is in Spanish. The model should classify the text even if it encounters another language, but primarily focus on Spanish.

A medical indication must contain the following:
- Clinic name and address
- Date
- Patient name
- Medical study
- Doctor name
- EXQ / Exequatur (doctor license number, typically 4-6 digits, sometimes with dashes)

If the text contains this information, classify it as 'Medical Indication'. Otherwise, classify it as 'Other'.

Text = {text}
Answer:
"""

# Example Data (Images)
image_paths = [
    "/assets/im.jpeg",
    "/assets/madelin_im.jpeg",
    "sh.jpg"
]

print("Starting...\n")

for image_path in image_paths:
    extracted_text = extract_text_from_image(image_path)
    response = llm([HumanMessage(content=prompt_template.format(text=extracted_text))])
    print(f"Image: {image_path}\nExtracted Text: {extracted_text}\nPrediction: {response.content}.\n")

print("\nFinished...")