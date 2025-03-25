from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, AgentType
from langchain.tools import tool, Tool
from langchain.sql_database import SQLDatabase
from langchain.memory import ConversationBufferMemory
from scripts.charts import (
    plot_anda_approvals_by_year,
    plot_applicants_by_year,
    plot_top_20_applicants_pie_range
)
from .prompts import AGENT_SYSTEM_PROMPT
import streamlit as st

open_api_key = st.secrets["OPENAI_API_KEY"]

# 🎯 Define tools as functions
@tool
def show_approvals_by_year() -> str:
    """Displays a chart of FDA ANDA approvals by year."""
    df = plot_anda_approvals_by_year(db_path="fda_first_generic_approvals.db", show=True)
    return "Chart of FDA ANDA approvals by year displayed below."

@tool
def show_applicants_by_year() -> str:
    """Displays a chart of unique applicants by year."""
    df = plot_applicants_by_year(db_path="fda_first_generic_approvals.db", show=True)
    return "Chart of unique applicants by year displayed below."

@tool
def show_top_20_applicants_range() -> str:
    """Displays a pie chart of the top 20 applicants from 2020 to 2024."""
    df = plot_top_20_applicants_pie_range(start_year=2020, end_year=2024, db_path="fda_first_generic_approvals.db", show=True)
    return "Chart of top 20 applicants (2020–2024) displayed below."

# 🚀 Agent creation with tools + memory
def create_sqlite_agent(db_path="fda_first_generic_approvals.db"):
    llm = ChatOpenAI(
        temperature=0,
        model="gpt-3.5-turbo",
        openai_api_key=open_api_key
    )

    tools = [
        Tool.from_function(show_approvals_by_year),
        Tool.from_function(show_applicants_by_year),
        Tool.from_function(show_top_20_applicants_range)
    ]

    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    agent_executor = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.OPENAI_FUNCTIONS,
        memory=memory,
        verbose=True,
        handle_parsing_errors=True,
        system_message=AGENT_SYSTEM_PROMPT
    )

    return agent_executor, memory
