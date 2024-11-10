import os
from dotenv import load_dotenv # type: ignore
from langchain_openai import ChatOpenAI # type: ignore
from langchain_core.pydantic_v1 import BaseModel, Field # type: ignore

# Load environment variables from the .env file
load_dotenv()

# Build an LLM abstraction
llm = ChatOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    model_name="gpt-3.5-turbo", # Here I'm being explicit, but this is the default model used by ChatOpenAI at the time of writing.
)

# Define a Pydantic model for structured output
class Joke(BaseModel):
    setup: str = Field(description="The setup of the joke")
    punchline: str = Field(description="The punchline to the joke")
    rating: str = Field(description="How funny the joke is, from 1 to 10")

# Using our ChatOpenAI llm model and configuring its structured output
structured_llm = llm.with_structured_output(Joke)

joke = structured_llm.invoke("Tell me a joke about cats")

print(f"{joke.setup} {joke.punchline} | Rating: {joke:rating}")