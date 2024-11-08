import os
from dotenv import load_dotenv # type: ignore
from langchain_openai import ChatOpenAI # type: ignore
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder # type: ignore
from langchain_core.messages import HumanMessage # type: ignore

# Load environment variables from the .env file
load_dotenv()

# Build an LLM abstraction
llm = ChatOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    model_name="gpt-3.5-turbo", # Here I'm being explicit, but this is the default model used by ChatOpenAI at the time of writing.
)

prompt_template = ChatPromptTemplate.from_messages([
    ("system", "You are a helful assistant"),
    MessagesPlaceholder("msgs")
])

prompt_template.invoke({"msgs": [HumanMessage(content="hi!")]})

prompt_template = ChatPromptTemplate.from_messages([
    ("system", "You are a helful assistant"),
    ("placeholder", "{msgs}") # <-- This is the changed part
])

template = prompt_template.invoke({
    "msgs": [HumanMessage(content="hi!")]
})
print(template)

chain = prompt_template | llm
llm_response = chain.invoke({
    "topic": "cats"
})
print("\n==== Start LLM Response ====\n")
print(llm_response.content)
print("\n==== End LLM Response ====\n")