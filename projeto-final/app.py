import streamlit as st
import asyncio
import uuid
from fastmcp import Client

# Set up page configuration
st.set_page_config(page_title="AI Database Assistant", layout="centered")

# Title
st.title("🤖 AI Database Assistant")
st.markdown("Ask questions about your database and get AI-powered insights")

# Unique user memory namespace
if "user_id" not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# Helper: Call the MCP agent server via SSE
async def call_agent(question: str):
    client = Client("http://127.0.0.1:8004/sse")  # Replace with your server URL
    async with client:
        result = await client.call_tool(
            "postgres-analyst",
            {"question": question},
        )
        return result[0].text if result and hasattr(result[0], "text") else str(result)


# Chat input
if prompt := st.chat_input("Ask me anything about the database..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response
    with st.chat_message("assistant"):
        with st.spinner("Analyzing your question..."):
            try:
                response = asyncio.run(call_agent(prompt))
                st.markdown(response)
                st.session_state.messages.append(
                    {"role": "assistant", "content": response}
                )
            except Exception as e:
                error_msg = f"Sorry, I encountered an error: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append(
                    {"role": "assistant", "content": error_msg}
                )

# Sidebar with info
with st.sidebar:
    st.header("ℹ️ About")
    st.markdown(
        """
    This AI assistant can help you:
    - Query your PostgreSQL database
    - Analyze data patterns
    - Generate insights
    - Answer questions about your data
    
    **User ID:** `{}`
    """.format(st.session_state.user_id[:8])
    )

    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")
    st.markdown("**Server:** `http://127.0.0.1:8004/sse`")
    st.markdown("**Tool:** `postgres-analyst`")
