#!/usr/bin/env python3

import gradio as gr
import chromadb
import os
from langchain_ollama import ChatOllama
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# Initialize Ollama and ChromaDB
OLLAMA_URL = "http://localhost:11434"
llm = ChatOllama(base_url=OLLAMA_URL, model="mistral:latest")

# ChromaDB setup
os.makedirs("05-memory/data", exist_ok=True)
chroma_client = chromadb.PersistentClient(path="05-memory/data")
collection = chroma_client.get_or_create_collection("user_conversations")

# In-memory stores for session management
chat_store = {}
long_term_memory = {}


def get_chat_history(session_id: str):
    if session_id not in chat_store:
        chat_store[session_id] = ChatMessageHistory()
    return chat_store[session_id]


def save_to_chromadb(user_id: str, message: str, is_human: bool):
    import time

    timestamp = str(int(time.time() * 1000))
    prefix = "Human: " if is_human else "AI: "
    collection.add(
        documents=[prefix + message],
        metadatas=[{"user_id": user_id, "type": "human" if is_human else "ai"}],
        ids=[f"{user_id}_{timestamp}"],
    )


def update_long_term_memory(session_id: str, input_text: str, output: str):
    if session_id not in long_term_memory:
        long_term_memory[session_id] = []
    if len(input_text) > 15:  # Store shorter messages too
        long_term_memory[session_id].append(f"User: {input_text}")
    if len(long_term_memory[session_id]) > 5:
        long_term_memory[session_id] = long_term_memory[session_id][-5:]


def get_long_term_memory(session_id: str):
    return ". ".join(long_term_memory.get(session_id, []))


# Updated prompt template for natural conversation
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a friendly and helpful AI assistant. Have natural conversations with users. "
            "Be conversational, warm, and personable. Keep your responses concise and engaging. "
            "Remember information about the user from previous conversations when relevant. "
            "Don't use any special formatting or thinking tags - just respond naturally like a human friend would.",
        ),
        ("system", "What you remember about this user: {long_term_memory}"),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}"),
    ]
)

chain = prompt | llm
chain_with_history = RunnableWithMessageHistory(
    chain, get_chat_history, input_messages_key="input", history_messages_key="history"
)


def chat_with_ai(message, user_id, history):
    if not message.strip():
        return history, ""

    try:
        print(f"Processing message: {message} for user: {user_id}")

        # Get AI response
        long_term_mem = get_long_term_memory(user_id)
        response = chain_with_history.invoke(
            {"input": message, "long_term_memory": long_term_mem},
            config={"configurable": {"session_id": user_id}},
        )

        # Extract and clean response content
        ai_response = (
            response.content if hasattr(response, "content") else str(response)
        )

        # Clean the response from any unwanted formatting
        ai_response = ai_response.replace("<think>", "").replace("</think>", "")
        ai_response = ai_response.strip()

        print(f"AI Response: {ai_response[:100]}...")

        # Update long-term memory
        update_long_term_memory(user_id, message, ai_response)

        # Save to ChromaDB
        save_to_chromadb(user_id, message, True)
        save_to_chromadb(user_id, ai_response, False)

        # Create new history with the conversation
        new_history = history.copy() if history else []
        new_history.append({"role": "user", "content": message})
        new_history.append({"role": "assistant", "content": ai_response})

        return new_history, ""

    except Exception as e:
        print(f"Error: {str(e)}")
        error_msg = "Sorry, I had a technical issue. Could you try again?"
        new_history = history.copy() if history else []
        new_history.append({"role": "user", "content": message})
        new_history.append({"role": "assistant", "content": error_msg})
        return new_history, ""


def view_chromadb_data():
    try:
        all_data = collection.get()
        if not all_data["documents"]:
            return "No conversations stored yet."

        output = "ChromaDB Stored Conversations:\n" + "=" * 50 + "\n"

        # Group by user and sort by timestamp
        user_data = {}
        for doc, metadata, doc_id in zip(
            all_data["documents"], all_data["metadatas"], all_data["ids"]
        ):
            user_id = metadata["user_id"]
            if user_id not in user_data:
                user_data[user_id] = []
            # Extract timestamp from id for sorting
            timestamp = doc_id.split("_")[-1] if "_" in doc_id else "0"
            user_data[user_id].append((timestamp, doc))

        for user_id, messages in user_data.items():
            output += f"\n--- User {user_id} ---\n"
            # Sort by timestamp to show conversation in order
            messages.sort(key=lambda x: x[0])
            for _, msg in messages:
                output += f"{msg}\n"

        return output
    except Exception as e:
        return f"Error loading ChromaDB data: {str(e)}"


def clear_user_data(user_id):
    # Clear from memory
    if user_id in chat_store:
        del chat_store[user_id]
    if user_id in long_term_memory:
        del long_term_memory[user_id]

    # Clear from ChromaDB
    try:
        results = collection.get(where={"user_id": user_id})
        if results["ids"]:
            collection.delete(ids=results["ids"])
    except Exception:
        pass

    return [], f"✅ Data cleared for User {user_id}"


def load_user_conversation(user_id):
    """Load existing conversation from ChromaDB for display"""
    try:
        results = collection.get(where={"user_id": user_id})
        if not results["documents"]:
            return []

        # Sort messages by timestamp for proper order
        messages_with_ids = list(zip(results["documents"], results["ids"]))
        messages_with_ids.sort(
            key=lambda x: x[1].split("_")[-1] if "_" in x[1] else "0"
        )

        history = []
        for doc, _ in messages_with_ids:
            if doc.startswith("Human: "):
                history.append({"role": "user", "content": doc[7:]})
            elif doc.startswith("AI: "):
                history.append({"role": "assistant", "content": doc[4:]})

        return history
    except Exception:
        return []


# Gradio Interface
with gr.Blocks(title="AI Agent Memory Demo") as demo:
    gr.Markdown("# 🤖 AI Agent Memory Demo with ChromaDB")
    gr.Markdown(
        "**Demo Purpose:** Show how AI agents can remember conversations using ChromaDB storage.\n\n"
        "• Select different User IDs to see separate conversation histories\n"
        "• Each user's conversation is stored independently\n"
        "• Switch between users to see memory persistence"
    )

    with gr.Row():
        with gr.Column(scale=2):
            user_dropdown = gr.Dropdown(
                choices=["1", "2", "3"],
                value="1",
                label="👤 Select User ID",
                info="Each user has their own conversation memory",
            )

            chatbot = gr.Chatbot(
                label="💬 Conversation",
                height=400,
                type="messages",
                show_copy_button=True,
            )

            with gr.Row():
                msg_input = gr.Textbox(
                    placeholder="Type your message...", label="Your Message", scale=4
                )
                send_btn = gr.Button("📤 Send", scale=1, variant="primary")

        with gr.Column(scale=1):
            gr.Markdown("### 🛠️ Memory Controls")

            view_db_btn = gr.Button("👀 View ChromaDB Data", variant="secondary")
            clear_btn = gr.Button("🗑️ Clear User Data", variant="stop")

            db_output = gr.Textbox(
                label="📊 ChromaDB Storage",
                lines=12,
                max_lines=20,
                info="Shows all stored conversations",
            )

    # Event handlers
    send_btn.click(
        chat_with_ai,
        inputs=[msg_input, user_dropdown, chatbot],
        outputs=[chatbot, msg_input],
    )

    msg_input.submit(
        chat_with_ai,
        inputs=[msg_input, user_dropdown, chatbot],
        outputs=[chatbot, msg_input],
    )

    view_db_btn.click(view_chromadb_data, outputs=db_output)

    clear_btn.click(clear_user_data, inputs=user_dropdown, outputs=[chatbot, db_output])

    # Load conversation when user changes
    user_dropdown.change(
        load_user_conversation, inputs=user_dropdown, outputs=[chatbot]
    )


if __name__ == "__main__":
    demo.launch(share=True)
