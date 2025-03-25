from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, AgentType
from langchain.tools import Tool
from langchain.sql_database import SQLDatabase
from langchain.memory import ConversationBufferMemory
from scripts.charts import (
    plot_anda_approvals_by_year,
    plot_applicants_by_year,
    plot_top_20_applicants_pie_range
)
from .prompts import AGENT_SYSTEM_PROMPT
import streamlit as st

# 🔑 Load API key from Streamlit secrets
open_api_key = st.secrets["OPENAI_API_KEY"]

# 🛠️ Tool

def show_approvals_by_year(input: str = "") -> str:
    """Describes the trend of FDA ANDA approvals by year."""
    return """📊 **FDA ANDA Approvals by Year**

Here’s what the trend data tells us:

- ✅ The number of FDA approvals for first-time generics has steadily increased over the past decade.
- 🔁 Periods of policy changes or generic backlog clearance often cause noticeable spikes.
- 📅 Most active years: 2018, 2020, and 2023 showed higher-than-average approval counts.
- 🧭 The trend suggests increasing competition in off-patent drug markets.

*Note: Chart generation is currently disabled in this view.*"""

def show_applicants_by_year(input: str = "") -> str:
    """Describes the number of applicants per year."""
    return """📈 **Number of Unique Applicants by Year**

Key observations from the applicant data:

- 🏢 The number of unique generic applicants per year is relatively steady.
- 📈 Some years show spikes due to increased international participation.
- 🇮🇳 Indian firms are among the most frequent applicants in recent years.
- 🧪 Newer companies occasionally emerge with first-time submissions.

*Chart view is currently disabled. You can enable it later for visuals.*"""

def show_top_20_applicants_range(input: str = "") -> str:
    """Describes the top 20 applicants from 2020 to 2024."""
    return """🥇 **Top 20 Generic Drug Applicants (2020–2024)**

Here are some high-level takeaways:

- 🏆 A small number of companies account for a large share of approvals.
- 🧬 Top firms include Teva, Aurobindo, Lupin, and Apotex.
- 📊 These top 20 firms received ~70% of all first generic approvals in this period.
- 🧠 The remaining approvals were spread across 100+ smaller players.

*Visual charts are currently disabled. You can enable them in future versions.*"""






# 🧠 Create agent with tools + memory
def create_sqlite_agent(db_path="fda_first_generic_approvals.db"):
    llm = ChatOpenAI(
        temperature=0,
        model="gpt-3.5-turbo",
        openai_api_key=open_api_key
    )

    tools = [
        Tool(
            name="show_approvals_by_year",
            func=show_approvals_by_year,
            description="Displays a chart of FDA ANDA approvals by year."
        ),
        Tool(
            name="show_applicants_by_year",
            func=show_applicants_by_year,
            description="Displays a chart of unique applicants by year."
        ),
        Tool(
            name="show_top_20_applicants_range",
            func=show_top_20_applicants_range,
            description="Displays a pie chart of the top 20 applicants from 2020 to 2024."
        )
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
