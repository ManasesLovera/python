import os
from dotenv import load_dotenv # type: ignore
# from langchain_community.chat_models import ChatOllama # The class `ChatOllama` was deprecated in LangChain 0.3.1 and will be removed in 1.0.0. An updated version of the class exists in the :class:`~langchain-ollama package and should be used instead.
from langchain_ollama.llms import OllamaLLM #type: ignore
from langchain_core.output_parsers import StrOutputParser #type: ignore
from langchain_core.prompts import ChatPromptTemplate #type: ignore

llm = OllamaLLM(
    base_url=os.getenv("CHATOLLAMA_BASE_URL"), 
    model="mistral:7b-instruct-v0.2-q2_K", # llama3.1
    temperature=0
)

prompt = ChatPromptTemplate.from_template("Translate {input} into {language}")

chain = prompt | llm | StrOutputParser()

result = chain.invoke({
    "input": "I love programming.",
    "language": "Frence"
})

print(result)