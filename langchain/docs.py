import getpass
import os
from dotenv import load_dotenv # type: ignore

# Load environment variables from the .env file
load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key or not openai_api_key.strip():
    openai_api_key = getpass.getpass("Enter your OpenaAI API key: ")

from langchain_openai import ChatOpenAI # type: ignore

llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    api_key=openai_api_key
)

print("Welcome to my translator app!")
languageFrom = input("Translate\nfrom: ")
languageTo = input("to: ")
text = input("Write the text you want to translate: ")
messages = [
    (
        "system",
        f"You are a helpful assistant that translate {languageFrom} to {languageTo}. Translate the user sentence.",
    ),
    (
        "human",
        f"{text}"
    )
]
ai_msg = llm.invoke(messages)
print(f"\nEl resultado es: \n\n{ai_msg.content}")