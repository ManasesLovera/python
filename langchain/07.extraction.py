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

from langchain_core.prompts import ChatPromptTemplate #type: ignore
from pydantic import BaseModel, Field, ValidationError # type: ignore
import json
from jsonschema.validators import Draft202012Validator # type: ignore

# Text extracted from OCR (Optical Character Recognition)

ocr_extracted_text = "We the People of the UNITED States, in order to form a more perfect UNION, establish Justice, insure domestic Tranquility, provide for the common defence, promote the general Welfare, and secure the Blessings of Liberty to ourselves and our Pastenty do ordain and establish this Constitution for the United States of America Calm Coal 3 SIGNATURE OF BEARER / SIGNATURE DU TITULAIRE / FIRMA DEL TITULAR PASSPORT PASSEPORT PASAPORTE UNITED STATES OF AMERICA Type/Type/Tipo Code/Code/Codigo Passport No./ No. du Passeport/No. de Pasaporte 596880807 Surname/Nom/Apellidos COOLEY USA Given Names/Prénoms / Nombres JOHNNIE CALVIN Nationality / Nationalité/ Nacionalidad UNITED STATES OF AMERICA Date of birth/Date de naissance/Fecha de nacimiento 19 Aug 1956 Place of birth/Lieu de naissance/Lugar de nacimiento MICHIGAN, U.S.A. Date of issue/Date de délivrance/Fecha de expedición 12 Sep 2019 Date of expiration/Date d'expiration / Fecha de caducidad 11 Sep 2029 Endorsements/Mantions Spéciales/Anotaciones SEE PAGE 27 Sex/Sexe/Sexo M Authority/Autorité / Autoridad United States Department of State USA P<USACOOLEY<<JOHNNIE<CALVIN<<<<<<<<<<<<<<<<< 5968808071USA5608191M2909118173306426<601164"

# Setup for the extraction algorithm
# The prefix is an instruction to the extraction algorithm to extract only relevant information
prefix = (
        "You are a top-tier algorithm for extracting information from text. "
        "Only extract information that is relevant to the provided text. "
        "If no information is relevant, use the schema and output "
        "an empty list where appropriate."
    )

# Create a system message tuple with the prefix
system_message = ("system", prefix)

# List to hold the components of the prompt
prompt_components = [system_message]

# Append the human message to the prompt components
# This message contains the text from which we want to extract information
prompt_components.append(
    (
        "human",
        "I need to extract information from "
        "the following text: ```\n{text}\n```\n"
    )
)

# Create a prompt template from the messages
# This template will format the input text for the language model
prompt_template = ChatPromptTemplate.from_messages(prompt_components)

from pydantic import BaseModel, Field # type: ignore
from datetime import datetime

# Define a Pydantic model for the Passport details
# This model will be used to structure the extracted information
class Passport(BaseModel):
    full_name: str = Field(..., description="The full name of the passport holder")
    passport_number: str = Field(..., description="The passport number")
    expiration_date: datetime = Field(..., description="The expiration date of the passport in ISO 8601 format")
    birth_date: datetime = Field(..., description="The birth date of the passport holder in ISO 8601 format")
    nationality: str = Field(..., description="The nationality of the passport holder")

# Combine the prompt template and the chat model to create a runnable sequence
# The chat model is configured to output data in the structure defined by the LLM
extr_runnable = (prompt_template | llm.with_structured_output(Passport)).with_config(
        {"run_name": "extraction"}
    )

# Invoke the runnable sequence with the OCR extracted text
# This will extract the passport details from the text and format it according to the LLM
passport = extr_runnable.invoke({"text": ocr_extracted_text})

# Print the extracted passport information
print(passport)

class ExtractorDefinition(BaseModel):
    """Define an information extractor to be used in an information extraction system."""

    json_schema: str = Field(
        ...,
        description=(
            "JSON Schema that describes the entity /"
            "information that should be extracted. "
            "This schema is specified in JSON Schema format. "
        )
    )

SUGGEST_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are are an expert ontologist and have been asked to help a user "
            "define an information extractor.The user will describe an entity, "
            "a topic or a piece of information that they would like to extract from "
            "text. Based on the user input, you are to provide a schema and "
            "description for the extractor. The schema should be a JSON Schema that "
            "describes the entity or information to be extracted. information to be "
            "extracted. Make sure to include title and description for all the "
            "attributes in the schema. The JSON Schema should describe a top level "
            "object. The object MUST have a title and description. Title must be in snake_case."
            "Make the description valid JSON schema values or do not add them at all."
            "Unless otherwise stated all entity properties in the schema should be considered optional.",
        ),
        ("human", "{input}")
    ]
)

suggestion_chain = SUGGEST_PROMPT | llm.with_structured_output(
    schema=ExtractorDefinition
).with_config({"run_name": "suggest"})

# This description will be generated from iterating over the elements within a set of datapoints for a given tag.
# There will be an attempt of keeping track of tokens to avoid adding information that might truncate the properties.
# Descriptions will be eliminated if a threshold is met
description = """
    Extract the following information:
    1. FULLNAME: A fullname is the complete legal name of an individual, typically including the first name, middle name(s), and last name. It represents a given and family names in full.
    2. PASSPORT NUMBER: A passport number is a unique identifier assigned to a passport, used to verify their identity and nationality. It is issued by the government of a country and is essential for international travel documentation and security checks.
    3. EXPIRATION DATE: An expiration date is the specific date after which a product or document is no longer valid or safe to use. It indicates the end of the period during which the item can be expected to function properly or remain effective, and is often formatted in ISO 8601 format (YYYY-MM-DD) for standardization and clarity.
    4. BIRTH DATE: A birth date is the specific date on which an individual was born, marking the beginning of their life. It is often formatted in ISO 8601 format (YYYY-MM-DD) for consistency and precision in records and documentation.
    5. NATIONALITY
    """
suggested_json_schema = None

try:
    suggested_json_schema = suggestion_chain.invoke({
        "input": description
    })
except ValidationError as e:
    print(e.errors()[0])
    suggested_json_schema = None

# Validate the suggested JSON schema
if suggested_json_schema:
  json_schema = json.loads(suggested_json_schema.json_schema)
  print(json.dumps(json_schema, indent=2))

  # Check if the schema itself is valid
  Draft202012Validator.check_schema(json_schema)
else:
  print("Failed to generate schema")

"""Structured extraction with a JSON Schema"""

if json_schema:
   extr_runnable = (prompt_template | llm.with_structured_output(json_schema)).with_config({
      "run_name": "extraction"
   })

   passport = extr_runnable.invoke({"text": ocr_extracted_text})

   print(f"Passport number: {passport['passport_number']}")