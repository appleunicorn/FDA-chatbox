from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, AgentType
from langchain.tools import Tool
from langchain.memory import ConversationBufferMemory
from scripts.charts import (
    plot_anda_approvals_by_year,
    plot_applicants_by_year,
    plot_top_20_applicants_pie_range
)
from .prompts import AGENT_SYSTEM_PROMPT
import streamlit as st

open_api_key = st.secrets["OPENAI_API_KEY"]

def show_approvals_by_year(input: str = "") -> dict:
    """Returns the data for FDA ANDA approvals by year chart."""
    df = plot_anda_approvals_by_year(db_path="fda_first_generic_approvals.db", show=False)
    return {
        "tool_result": "approvals_by_year_chart",
        "data": df.to_json()
    }

def show_applicants_by_year(input: str = "") -> dict:
    """Returns the data for number of applicants by year chart."""
    df = plot_applicants_by_year(db_path="fda_first_generic_approvals.db", show=False)
    return {
        "tool_result": "applicants_by_year_chart",
        "data": df.to_json()
    }

def show_top_20_applicants_range(input: str = "") -> dict:
    """Returns the data for top 20 applicants (2020–2024) pie chart."""
    df = plot_top_20_applicants_pie_range(start_year=2020, end_year=2024, db_path="fda_first_generic_approvals.db", show=False)
    return {
        "tool_result": "top_20_applicants_chart",
        "data": df.to_json()
    }

def create_sqlite_agent(db_path="fda_first_generic_approvals.db"):
    llm = ChatOpenAI(
        temperature=0,
        model="gpt-3.5-turbo",
        openai_api_key=open_api_key
    )

    tools = [
        Tool(name="show_approvals_by_year", func=show_approvals_by_year, description="Return chart data for FDA ANDA approvals by year."),
        Tool(name="show_applicants_by_year", func=show_applicants_by_year, description="Return chart data for number of applicants by year."),
        Tool(name="show_top_20_applicants_range", func=show_top_20_applicants_range, description="Return chart data for top 20 applicants from 2020 to 2024.")
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
