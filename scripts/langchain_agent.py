from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain_community.agent_toolkits.sql.base import SQLDatabaseToolkit as CommunitySQLToolkit
from langchain.sql_database import SQLDatabase
from langchain.chat_models import ChatOpenAI
import os

import os
import streamlit as st
os.environ["OPENAI_API_KEY"] = st.secrets["openai_key"]

def create_sqlite_agent(db_path="fda_first_generic_approvals.db"):
    llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo") # type: ignore
    db_uri = f"sqlite:///{db_path}"
    db = SQLDatabase.from_uri(db_uri)

    toolkit = CommunitySQLToolkit(db=db, llm=llm)
    agent_executor = create_sql_agent(
        llm=llm,
        toolkit=toolkit,
        verbose=True,
        agent_type="openai-functions",  # or "chat-zero-shot-react-description" # type: ignore
        handle_parsing_errors=True
    )
    return agent_executor
