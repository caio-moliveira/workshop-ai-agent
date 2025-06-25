import streamlit as st
import asyncio
from fastmcp import Client

st.title("MCP Agent Chat")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# Call MCP agent
async def call_agent(question: str):
    client = Client("http://127.0.0.1:8004/sse")
    async with client:
        result = await client.call_tool("context7_analyst", {"question": question})
        # Extract the actual content from the result
        if result and hasattr(result[0], "content"):
            return result[0].content
        elif result and hasattr(result[0], "text"):
            return result[0].text
        else:
            return str(result)


# Chat input
if prompt := st.chat_input("Ask anything..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get agent response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = asyncio.run(call_agent(prompt))
                st.markdown(response)
                st.session_state.messages.append(
                    {"role": "assistant", "content": response}
                )
            except Exception as e:
                error_msg = f"Error: {e}"
                st.error(error_msg)
                st.session_state.messages.append(
                    {"role": "assistant", "content": error_msg}
                )
