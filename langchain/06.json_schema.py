import os
from dotenv import load_dotenv # type: ignore
from langchain_openai import ChatOpenAI # type: ignore

from typing import Any, Dict 
from jsonschema import exceptions # type: ignore
from jsonschema.validators import Draft202012Validator # type: ignore

# Load environment variables from the .env file
load_dotenv()

# Build an LLM abstraction
llm = ChatOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    model_name="gpt-3.5-turbo", # Here I'm being explicit, but this is the default model used by ChatOpenAI at the time of writing.
)

def validate_json_schema(schema: Dict[str, Any]) -> None:
    """Validate a JSON schema."""
    try:
        Draft202012Validator.check_schema(schema)
    except exceptions.ValidationError as e:
        raise Exception(
            f"Not a valid JSON schema: {e.message}"
        )

json_schema = {
    "title": "joke", # The title of the schema
    "description": "Joke to tell user.",
    "type": "object",
    "properties": {
        "setup": {
            "type": "string",
            "description": "The setup of the joke"
        },
        "punchline": {
            "type": "string",
            "description": "The punchline to the joke"
        }
    },
    "required": ["setup", "punchline"]
}

try:
    Draft202012Validator.check_schema(json_schema)

    structured_llm = llm.with_structured_output(json_schema)

    joke = structured_llm.invoke("Tell me a joke about cats")

    print(f"{joke['setup']} {joke['punchline']} | Rating: {joke.get('rating', 'No rating provided')}")

except exceptions.ValidationError as e:

    raise Exception(f'Invalid schema: {e.message}')