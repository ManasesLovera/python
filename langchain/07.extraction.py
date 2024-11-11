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
