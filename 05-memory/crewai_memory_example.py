import os
from pathlib import Path

from crewai import Agent, Task, Crew, Process
from crewai.memory.short_term.short_term_memory import ShortTermMemory
from crewai.memory.long_term.long_term_memory import LongTermMemory
from crewai.memory.entity.entity_memory import EntityMemory
from crewai.memory.storage.rag_storage import RAGStorage
from crewai.memory.storage.ltm_sqlite_storage import LTMSQLiteStorage
from langchain_openai import ChatOpenAI


class FriendlyAI:
    """Friendly AI agent using CrewAI's explicit memory system with ChromaDB"""

    def __init__(self, openai_api_key: str = None, storage_dir: str = None):
        # Set up OpenAI API key
        if openai_api_key:
            os.environ["OPENAI_API_KEY"] = openai_api_key
        elif not os.getenv("OPENAI_API_KEY"):
            raise ValueError(
                "OpenAI API key must be provided either as parameter or environment variable"
            )

        # Get the API key for explicit configuration
        self.openai_api_key = os.getenv("OPENAI_API_KEY")

        # Set up storage directory - use repository structure
        if storage_dir is None:
            # Get the project root directory (where this script is located)
            project_root = Path(__file__).parent.absolute()
            # Set storage to root/05-memory/crewai_memory/
            storage_dir = project_root / "crewai_memory"
        else:
            storage_dir = Path(storage_dir)

        # Create the directory if it doesn't exist
        storage_dir.mkdir(parents=True, exist_ok=True)

        # Set the environment variable for CrewAI
        os.environ["CREWAI_STORAGE_DIR"] = str(storage_dir)

        # Store the path for later reference
        self.storage_dir = storage_dir

        # Initialize LLM
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

    def chat(self, message: str) -> str:
        """Main chat method - creates agent, task, crew and processes user message"""

        # Create the friendly agent
        agent = Agent(
            role="Friendly Companion",
            goal="Be a warm, supportive, and engaging friend who remembers our conversations and provides thoughtful, contextual responses",
            backstory="""You're a caring and empathetic friend who loves to chat about anything and everything. 
            You have an excellent memory and remember what we've talked about before, which helps you provide 
            more meaningful and personalized responses. You're funny when appropriate, supportive when needed, 
            and always authentic. You speak naturally, like you're texting a close friend - casual but caring.
            
            You use your memory to:
            - Remember previous conversations and topics we've discussed
            - Recall personal details the user has shared
            - Build on past interactions to deepen our friendship
            - Provide continuity across conversations
            - Show genuine interest by referencing things we've talked about before""",
            verbose=False,
            llm=self.llm,
            allow_delegation=False,
        )

        # Create a task for this specific conversation
        chat_task = Task(
            description=f"""
            The user just said: "{message}"
            
            As their friendly AI companion, respond warmly and naturally. Use your memory to:
            
            1. **Remember context**: Recall previous conversations, topics we've discussed, 
               and any personal details the user has shared
            
            2. **Build continuity**: Reference past interactions when relevant to show 
               you remember and care about our ongoing friendship
            
            3. **Be authentic**: Respond like a close friend would - warm, supportive, 
               sometimes funny, always genuine
            
            4. **Stay contextual**: Use your memory to provide responses that feel 
               connected to our relationship history
            
            Important: 
            - Keep responses conversational and friendly, like texting a good friend
            - Show you remember previous conversations when relevant
            - Be supportive and engaging
            - Ask follow-up questions when appropriate to deepen the conversation
            
            Current message to respond to: "{message}"
            """,
            agent=agent,
            expected_output="""A friendly, warm, and engaging response that:
            - Feels natural and conversational
            - Shows memory of past interactions when relevant
            - Demonstrates care and interest in the user
            - Is appropriate to the tone and content of the user's message
            - Maintains the feeling of an ongoing friendship""",
        )

        # Create the crew with explicit memory configuration
        crew = Crew(
            agents=[agent],
            tasks=[chat_task],
            process=Process.sequential,
            verbose=False,
            memory=True,
            # Long-term memory using SQLite storage
            long_term_memory=LongTermMemory(
                storage=LTMSQLiteStorage(
                    db_path=str(self.storage_dir / "long_term_memory_storage.db")
                )
            ),
            # Short-term memory using ChromaDB
            short_term_memory=ShortTermMemory(
                storage=RAGStorage(
                    type="short_term",
                    allow_reset=True,
                    embedder_config={
                        "provider": "openai",
                        "config": {
                            "model": "text-embedding-ada-002",
                            "api_key": self.openai_api_key,
                        },
                    },
                    crew=None,  # Will be set after crew creation
                    path=str(self.storage_dir / "short_term"),
                ),
            ),
            # Entity memory using ChromaDB
            entity_memory=EntityMemory(
                storage=RAGStorage(
                    type="entities",
                    allow_reset=True,
                    embedder_config={
                        "provider": "openai",
                        "config": {
                            "model": "text-embedding-ada-002",
                            "api_key": self.openai_api_key,
                        },
                    },
                    crew=None,  # Will be set after crew creation
                    path=str(self.storage_dir / "entities"),
                ),
            ),
        )

        # Execute the crew and get response
        result = crew.kickoff()

        # Extract the response text
        response = str(result).strip()

        return response


# Example usage with interactive chat
def interactive_chat():
    """Run an interactive chat session"""
    try:
        friend = FriendlyAI()

        print("🤖 CrewAI Friendly Agent with ChromaDB Memory")
        print("=" * 50)
        print("👋 Hey there! I'm your AI friend with ChromaDB-powered memory!")
        print("I'll remember our conversations using ChromaDB for fast retrieval.")
        print(f"📁 Memory stored in: {friend.storage_dir}")
        print("\nType 'quit' or 'exit' to end our chat")
        print("-" * 50)

        while True:
            user_input = input("\n💬 You: ").strip()

            if user_input.lower() in ["quit", "exit", "bye"]:
                response = friend.chat("I need to go now, goodbye!")
                print(f"🤖 Agent: {response}")
                break

            elif user_input:
                print("\n🤖 Agent: ", end="", flush=True)
                response = friend.chat(user_input)
                print(response)

        print(f"\n📊 Session complete! Memory is saved in: {friend.storage_dir}")

    except ValueError as e:
        print(f"❌ Error: {e}")
        print("\n🔧 Setup Instructions:")
        print("1. Set your OpenAI API key:")
        print("   export OPENAI_API_KEY='your-api-key-here'")
        print("2. Install dependencies:")
        print("   pip install crewai langchain-openai chromadb")
    except Exception as e:
        print(f"❌ An error occurred: {e}")


if __name__ == "__main__":
    # Run interactive chat
    interactive_chat()

    # Example of programmatic usage:
    """
    # Initialize the friend
    chat = FriendlyAI()
    
    # Have a conversation
    response1 = chat.chat("Hi! My name is Alex and I love hiking.")
    print(f"Response 1: {response1}")
    
    response2 = chat.chat("What's your favorite outdoor activity?")
    print(f"Response 2: {response2}")
    
    # The agent will remember Alex's name and interest in hiking
    response3 = chat.chat("I went on a great hike yesterday!")
    print(f"Response 3: {response3}")
    """
