from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain_community.agent_toolkits.sql.base import SQLDatabaseToolkit as CommunitySQLToolkit
from langchain.sql_database import SQLDatabase
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
import streamlit as st
from .prompts import AGENT_SYSTEM_PROMPT

open_api_key = st.secrets["OPENAI_API_KEY"]

def create_sqlite_agent(db_path="fda_first_generic_approvals.db"):
    llm = ChatOpenAI(
        temperature=0,
        model="gpt-3.5-turbo",
        openai_api_key=open_api_key
    )

    db_uri = f"sqlite:///{db_path}"
    db = SQLDatabase.from_uri(db_uri)
    toolkit = CommunitySQLToolkit(db=db, llm=llm)

    # ✅ Memory to track conversation
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    agent_executor = create_sql_agent(
        llm=llm,
        toolkit=toolkit,
        verbose=True,
        agent_type="openai-functions",
        handle_parsing_errors=True,
        memory=memory,
        system_message=AGENT_SYSTEM_PROMPT
    )
    return agent_executor, memory
