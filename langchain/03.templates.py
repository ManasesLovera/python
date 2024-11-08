import os
from dotenv import load_dotenv # type: ignore
from langchain_openai import ChatOpenAI #type: ignore
from langchain.chains import LLMChain #type: ignore
from langchain_core.runnables import RunnableSequence, RunnableLambda #type: ignore
from langchain_core.prompts import ChatPromptTemplate #type: ignore

# Load environment variables from the .env file
load_dotenv()

prompt = ChatPromptTemplate.from_template("Translate {input} into {language}")
chat = ChatOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    model_name="gpt-3.5-turbo"
)

prompt.invoke({
    "input": "How are you?",
    "language": "Spanish"
})

# The class `LLMChain` was deprecated in LangChain 0.1.17 and will be removed in 1.0. Use :meth:`~RunnableSequence, e.g., `prompt | llm`` instead.
chain = LLMChain(llm=chat, prompt=prompt)
response = chain.invoke({
    "input": "How are you?",
    "language": "Spanish"
})
print(f'Using LLMChain: {response["text"]}')


chain = prompt | chat
result = chain.invoke({
    "input": "How are you?", 
    "language": "Spanish"
})
print(f'Using Runnable interface with LCEL: {result.content}')
