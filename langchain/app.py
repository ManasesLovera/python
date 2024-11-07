import os
from dotenv import load_dotenv # type: ignore
from langchain_openai import ChatOpenAI # type: ignore

# Load environment variables from the .env file
load_dotenv()

# Build an LLM abstraction
llm = ChatOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    model_name="gpt-4o", # Here I'm being explicit, but this is the default model used by ChatOpenAI at the time of writing.
)

# Pass a prompt directly
result = llm.invoke("Tell me a joke")

# Print the result
print(f"{result.content}\n\n ^^^\nJOKE\n\n\n")


"""
Langchain Community
"""

# LangChain supports many other chat models. Here, we're using Ollama
from langchain_community.chat_models import ChatOllama # type: ignore
from langchain_core.output_parsers import StrOutputParser # type: ignore
from langchain_core.prompts import ChatPromptTemplate # type: ignore

# supports many more optional parameters. Hover on your `ChatOllama(...)`
# class to view the latest available supported parameters

llm = ChatOllama(base_url=os.getenv("CHATOLLAMA_BASE_URL"), model="mistral:7b-instruct-v0.2-q2_K", temperature=0)

prompt = ChatPromptTemplate.from_template("Translate {input} into {language}")

# using LangChain Expressive Language chain syntax
# learn more about the LCEL on
# /docs/concepts/#langchain-expression-language-lcel
chain = prompt | llm | StrOutputParser() # type: ignore

# for brevity, response is printed in terminal
# You can use LangServe to deploy your application for production
result = chain.invoke({"input": "I love programming.", "language": "French"})

print(f"Translation: {result}")


"""
Chat Templates
"""

from langchain.chains import LLMChain # type: ignore
from langchain_core.runnables import RunnableSequence, RunnableLambda # type: ignore
from langchain_core.prompts import ChatPromptTemplate # type: ignore

prompt = ChatPromptTemplate.from_template("Translate {input} into {language}")
chat = ChatOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

prompt.invoke({"input": "How are you?", "language": "Spanish"})

# Create a chain with the LLM and prompt
chain = prompt | chat

# Invoke the chain with the input parameters
response = chain.invoke({"input": "How are you?", "language": "Spanish"})

# Print the response
print(f"Using LLMChain: {response["text"]}")

# Runnable sequence (using LCEL)
chain = RunnableSequence([prompt, llm])

result = chat.invoke({"input": "How are you?", "language": "Spanish"})
print(f"Using Runnable interface with LCEL: {result.content}")



"""
Using chat message list
"""

# from langchain_core.prompts import ChatPromptTemplate    / already imported

prompt_template = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant"),
    ("user", "Tell me a joke about {topic}")
])

templ = prompt_template.invoke({"topic": "cats"})

chain = prompt_template | llm
llm_resp = chain.invoke({"topic": "cats"})
print("\n==== Start LLM Response ====\n")
print(llm_resp.content)
print("\n==== End LLM Response ====\n")


