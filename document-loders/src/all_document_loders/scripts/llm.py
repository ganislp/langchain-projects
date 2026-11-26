import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage,HumanMessage
from langchain_core.prompts import SystemMessagePromptTemplate,HumanMessagePromptTemplate,ChatPromptTemplate,ChatMessagePromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv(override=True)
MODEL = "qwen/qwen3.8-27b"
openrouter_llm = ChatOpenAI(
    model=MODEL,
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)
parser = StrOutputParser()

system_message = SystemMessage("""You are helpful AI assistant who answer user question based on the provided context.""")


user_message = HumanMessage("""Answer user question based on the provided context ONLY! 
                              If you do not know the answer, just say "I don't know".
            ### Context:
            {context}

            ### Question:
            {question}

            ### Answer:""")
system_prompt = SystemMessagePromptTemplate.from_template(system_message.content)
user_prompt = HumanMessagePromptTemplate.from_template(user_message.content)

messages = [system_prompt,user_prompt]

template = ChatPromptTemplate.from_messages(messages)

chain = template | openrouter_llm | parser


def call_llm(context,question):
    return chain.invoke({"context":context,"question":question})