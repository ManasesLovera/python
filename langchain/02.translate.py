import os
from dotenv import load_dotenv # type: ignore
# from langchain_community.chat_models import ChatOllama # The class `ChatOllama` was deprecated in LangChain 0.3.1 and will be removed in 1.0.0. An updated version of the class exists in the :class:`~langchain-ollama package and should be used instead.
from langchain_core.output_parsers import StrOutputParser #type: ignore
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI #type: ignore

# Load environment variables from the .env file
load_dotenv()

llm = ChatOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    model_name="gpt-3.5-turbo", # Here I'm being explicit, but this is the default model used by ChatOpenAI at the time of writing.
)

prompt = ChatPromptTemplate.from_template("Translate {input} into {language}")

chain = prompt | llm | StrOutputParser()

result = chain.invoke({
    "input": "meine mutter ist Denisa.",
    "language": "Spanish"
})

print(result)

result = chain.invoke({
    "input": "Ich bin gut",
    "language": "Spanish"
})

print(result)