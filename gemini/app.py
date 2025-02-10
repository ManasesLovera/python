import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

gemini_api_key = os.getenv('GEMINI_API_KEY')

client = genai.Client(api_key=gemini_api_key)

response = client.models.generate_content_stream(
    model="gemini-2.0-flash-thinking-exp-01-21",
    contents = "Explain how AI works"
)

for chunk in response:
    print(chunk.text, end="")