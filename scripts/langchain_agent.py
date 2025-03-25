from langchain.chat_models import ChatOpenAI
from langchain.agents import create_sql_agent
from langchain.sql_database import SQLDatabase
from langchain.memory import ConversationBufferMemory
from .prompts import AGENT_SYSTEM_PROMPT
import streamlit as st

open_api_key = st.secrets["OPENAI_API_KEY"]

def create_sqlite_agent(db_path="fda_first_generic_approvals.db"):
    llm = ChatOpenAI(
        temperature=0,
        model="gpt-3.5-turbo",
        openai_api_key=open_api_key
    )

    db_uri = f"sqlite:///{db_path}"
    db = SQLDatabase.from_uri(db_uri)

    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    agent_executor = create_sql_agent(
        llm=llm,
        db=db,
        verbose=True,
        agent_type="openai-functions",
        handle_parsing_errors=True,
        memory=memory,
        system_message=AGENT_SYSTEM_PROMPT
    )

    return agent_executor, memory
