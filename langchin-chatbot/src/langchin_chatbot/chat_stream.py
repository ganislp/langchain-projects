import os
import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage,HumanMessage,ToolMessage
from langchain_core.prompts import HumanMessagePromptTemplate,SystemMessagePromptTemplate,ChatPromptTemplate,MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain_core.output_parsers import StrOutputParser

load_dotenv(override=True)
parser = StrOutputParser()
llm = ChatOpenAI(model="gpt-5.4-mini")
user_id = st.text_input("Enter your user id","ganesh-1201")

def get_chat_session(session_id:str):
    return SQLChatMessageHistory(session_id=session_id,connection="sqlite:///chat_history.db")


system_message = SystemMessage("Your are a helpful assistant")
user_message = HumanMessage("{input}")

system_prompt = SystemMessagePromptTemplate.from_template(system_message.content)
user_prompt = HumanMessagePromptTemplate.from_template(user_message.content)

messages = ChatPromptTemplate([system_prompt,user_prompt,MessagesPlaceholder(variable_name="history")])

chain = messages | llm | parser

runnable_chat_history = RunnableWithMessageHistory(chain,get_session_history=get_chat_session,input_messages_key="input",history_messages_key="history")

def chat_with_llm(input,session_id):
    for output in runnable_chat_history.stream({"input":input},
                                          config={"configurable":{"session_id":session_id}}):
     yield output

st.title("Make Ganesh Chatbot")
st.write("Chat with me!")

if "chat_history" not in st.session_state:
     st.session_state.chat_history = []   

if st.button("Start New Conversion"):
    st.session_state.chat_history = []
    history = get_chat_session(user_id)
    history.clear()

for message in  st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message['content'])   


prompt = st.chat_input("what is up?")
# st.write(prompt)

if prompt:
    st.session_state.chat_history.append({'role':'user','content':prompt})
    with st.chat_message("user"):
        st.markdown(prompt)   
    response = chat_with_llm(prompt,user_id)
    with st.chat_message("assistant"):
            st.write_stream(chat_with_llm(prompt,user_id))
    st.session_state.chat_history.append({'role':'assistant','content':response})        
