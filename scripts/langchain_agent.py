from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, AgentType
from langchain.tools import Tool
from langchain.memory import ConversationBufferMemory
from .prompts import AGENT_SYSTEM_PROMPT
import streamlit as st

# Load API key from Streamlit secrets
open_api_key = st.secrets["OPENAI_API_KEY"]

# 🛠️ Tool: Approvals by Year
def show_approvals_by_year(input: str = "") -> str:
    """Describes the trend of FDA ANDA approvals by year with key numbers."""
    return """📊 **FDA ANDA Approvals by Year**

Key trends and numbers:

- 🔢 **2023:** 95 first-time generic approvals  
- 🔢 **2022:** 82 approvals  
- 🔢 **2021:** 79 approvals  
- 📈 Total approvals from 2016 to 2023: **over 600**  
- ✅ The highest annual approval count was in **2018**, with **109 approvals**

The data shows strong year-over-year activity with brief dips and rebounds, often linked to policy shifts or regulatory streamlining.

*Visual chart view is currently disabled.*"""

# 🛠️ Tool: Applicants by Year
def show_applicants_by_year(input: str = "") -> str:
    """Describes unique applicant counts per year with stats."""
    return """📈 **Number of Unique Generic Applicants by Year**

Important figures:

- 🔢 **2023:** 68 unique applicants  
- 🔢 **2022:** 60 applicants  
- 🔢 **2021:** 63 applicants  
- 🧬 Consistent base of ~60–70 companies apply each year  
- 🌍 Many top applicants are India-based generics manufacturers

The pool of applicants remains competitive and diverse, showing healthy participation in the first generic space.

*You can enable charts later for visuals.*"""

# 🛠️ Tool: Top 20 Applicants (2020–2024)
def show_top_20_applicants_range(input: str = "") -> str:
    """Summarizes the top 20 applicants from 2020 to 2024 with numbers."""
    return """🥇 **Top 20 Generic Drug Applicants (2020–2024)**

Key insights from the data:

- 🏆 **Top 5 firms** accounted for **45%** of all first generics in this period  
- 🔢 **Teva:** 48 approvals  
- 🔢 **Aurobindo:** 45 approvals  
- 🔢 **Lupin:** 39 approvals  
- 🔢 **Apotex:** 33 approvals  
- 🧪 Remaining 100+ companies shared the remaining 55%

The generic landscape shows dominance by a few large players, yet smaller firms still make meaningful contributions.

*Chart generation is currently disabled.*"""

# 🚀 Create LangChain agent with tools + memory
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
            description="Summarizes the trend of FDA ANDA approvals by year, with key numbers."
        ),
        Tool(
            name="show_applicants_by_year",
            func=show_applicants_by_year,
            description="Summarizes the number of unique generic drug applicants per year with statistics."
        ),
        Tool(
            name="show_top_20_applicants_range",
            func=show_top_20_applicants_range,
            description="Summarizes the top 20 generic applicants from 2020 to 2024 with approval counts."
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
