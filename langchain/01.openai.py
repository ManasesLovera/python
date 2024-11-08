import os
from dotenv import load_dotenv # type: ignore
from langchain_openai import ChatOpenAI # type: ignore

# Load environment variables from the .env file
load_dotenv()

# Build an LLM abstraction
llm = ChatOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    model_name="gpt-3.5-turbo", # Here I'm being explicit, but this is the default model used by ChatOpenAI at the time of writing.
)

# Pass a prompt directly
result = llm.invoke("Tell me a joke")

# Print the result
print(f"{result.content}")