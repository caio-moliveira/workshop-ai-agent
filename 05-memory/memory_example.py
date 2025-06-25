#!/usr/bin/env python3

from langchain_ollama.llms import OllamaLLM
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from dotenv import load_dotenv
import os

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
OLLAMA_URL = "http://localhost:11434"
# Initialize the LLM
# llm = ChatOpenAI(model="gpt-4o-mini", max_tokens=1000, temperature=0)
llm = OllamaLLM(base_url=OLLAMA_URL, model="deepseek-r1:8b")

chat_store = {}
long_term_memory = {}


def get_chat_history(session_id: str):
    if session_id not in chat_store:
        chat_store[session_id] = ChatMessageHistory()
    return chat_store[session_id]


def update_long_term_memory(session_id: str, input: str, output: str):
    if session_id not in long_term_memory:
        long_term_memory[session_id] = []
    if len(input) > 20:
        long_term_memory[session_id].append(f"User said: {input}")
    if len(long_term_memory[session_id]) > 5:
        long_term_memory[session_id] = long_term_memory[session_id][-5:]


def get_long_term_memory(session_id: str):
    return ". ".join(long_term_memory.get(session_id, []))


prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful AI assistant. Use the information from long-term memory if relevant.",
        ),
        ("system", "Long-term memory: {long_term_memory}"),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}"),
    ]
)

chain = prompt | llm
chain_with_history = RunnableWithMessageHistory(
    chain, get_chat_history, input_messages_key="input", history_messages_key="history"
)


def chat(input_text: str, session_id: str):
    long_term_mem = get_long_term_memory(session_id)
    response = chain_with_history.invoke(
        {"input": input_text, "long_term_memory": long_term_mem},
        config={"configurable": {"session_id": session_id}},
    )
    update_long_term_memory(session_id, input_text, response.content)
    return response.content


session_id = "user_123"

print("AI:", chat("Hello! My name is Alice.", session_id))
print("AI:", chat("What's the weather like today?", session_id))
print("AI:", chat("I love sunny days.", session_id))
print("AI:", chat("Do you remember my name?", session_id))

print("Conversation History:")
for message in chat_store[session_id].messages:
    print(f"{message.type}: {message.content}")

print("\nLong-term Memory:")
print(get_long_term_memory(session_id))
