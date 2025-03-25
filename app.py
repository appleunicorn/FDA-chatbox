import pandas as pd
import altair as alt

# --- 💬 Chatbot Section ---
st.subheader("💬 Chat with the Data")

DB_PATH = "fda_first_generic_approvals.db"

if "agent" not in st.session_state or "memory" not in st.session_state:
    agent, memory = create_sqlite_agent(db_path=DB_PATH)
    st.session_state.agent = agent
    st.session_state.memory = memory

question = st.text_input(
    "Ask a question about the FDA approval data:",
    placeholder="e.g., Show chart of approvals by year"
)

if question:
    with st.spinner("🤖 Thinking..."):
        try:
            response = st.session_state.agent.run(question)

            if isinstance(response, dict) and "tool_result" in response:
                chart_type = response["tool_result"]
                df = pd.read_json(response["data"])

                st.markdown("### ✅ Chart Result")

                if chart_type == "approvals_by_year_chart":
                    st.bar_chart(df.set_index("year")["approvals"])
                elif chart_type == "applicants_by_year_chart":
                    st.line_chart(df.set_index("year")["num_applicants"])
                elif chart_type == "top_20_applicants_chart":
                    st.dataframe(df)
                else:
                    st.warning("Received unknown chart format.")
            else:
                st.markdown("### ✅ Answer")
                st.write(response)

        except Exception as e:
            st.error(f"Error: {e}")

# Show chat history
if st.session_state.memory.buffer:
    st.markdown("---")
    st.subheader("🧠 Chat History")
    for msg in st.session_state.memory.chat_memory.messages:
        role = "You" if msg.type == "human" else "Bot"
        st.markdown(f"**{role}:** {msg.content}")
