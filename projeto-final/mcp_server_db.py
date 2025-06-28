import os
import logging
from dotenv import load_dotenv
from fastmcp import FastMCP
from langchain_openai import ChatOpenAI
from crewai import Agent, Task, Crew, Process
from crewai_tools import MCPServerAdapter
from mcp import StdioServerParameters
from crewai.knowledge.source.crew_docling_source import CrewDoclingSource
from crewai.knowledge.storage.knowledge_storage import KnowledgeStorage

# -----------------------------
# Setup logging & environment
# -----------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
load_dotenv()

# -----------------------------
# Initialize FastMCP instance
# -----------------------------
mcp = FastMCP("postgres-analyst")

# -----------------------------
# Configuration
# -----------------------------
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://agent:MbDsofpeVAfehfII5H1oVJ13bd37FlLd@dpg-d1fttjvfte5s73fvhtfg-a.oregon-postgres.render.com/workshop_ai_agent?sslmode=require",
)

# Initialize LLM
llm = ChatOpenAI(
    model="gpt-4o-mini", temperature=0.1, api_key=os.getenv("OPENAI_API_KEY")
)


# -----------------------------
# Knowledge Management
# -----------------------------
def load_knowledge_sources():
    """Load documentation files into a Docling knowledge source."""
    try:
        return CrewDoclingSource(
            file_paths=[
                "01_schema_overview.md",
                "02_table_definitions.md",
                "03_kpi_definitions.md",
            ],
            storage=KnowledgeStorage(
                embedder={
                    "provider": "ollama",
                    "model": "mxbai-embed-large",
                    "base_url": "http://localhost:11434",
                }
            ),
        )
    except Exception as e:
        logger.warning(f"Failed to load knowledge sources: {e}")
        return None


# -----------------------------
# Core Agent Function
# -----------------------------
def run_postgres_analyst(question: str, user_id: str = "default") -> str:
    """
    Core function that creates and runs the Postgres analyst agent.
    """
    mcp_server_adapter = None

    try:
        # Setup MCP Server connection
        logger.info("Initializing MCP server connection...")
        serverparams = StdioServerParameters(
            command="npx",
            args=[
                "-y",
                "@modelcontextprotocol/server-postgres",
                DATABASE_URL,
            ],
        )

        mcp_server_adapter = MCPServerAdapter(serverparams)
        tools = mcp_server_adapter.tools

        if not tools:
            return "Error: No tools available from MCP server"

        logger.info(f"Connected to MCP server with {len(tools)} tools")

        # Load knowledge base
        knowledge = load_knowledge_sources()
        knowledge_sources = [knowledge] if knowledge else []

        # Create Agent
        agent = Agent(
            role="PostgreSQL Database Analyst",
            goal="Answer database questions using SQL queries with accurate, verified information",
            backstory=(
                "You are an expert SQL analyst with deep knowledge of PostgreSQL. "
                "You write efficient queries, understand database schemas, and provide "
                "precise answers based on actual data. You always verify schema before querying."
            ),
            tools=tools,
            knowledge_sources=knowledge_sources,
            llm=llm,
            allow_delegation=False,
            memory=False,
            verbose=True,
            max_iter=5,
            max_execution_time=180,
        )

        # Create Task
        task = Task(
            description=(
                f"Answer this database question: '{question}'\n\n"
                "PROCESS:\n"
                "1. First, check knowledge base for schema information\n"
                "2. If schema unclear, query information_schema tables\n"
                "3. Write and execute ONE precise SQL query\n"
                "4. Return the direct answer with key insights\n"
                "5. If no data found, state that clearly\n\n"
                "REQUIREMENTS:\n"
                "- Use only verified schema information\n"
                "- Write efficient, readable SQL\n"
                "- Provide concise, accurate answers\n"
                "- Include relevant numbers/metrics when applicable"
            ),
            expected_output="SQL query results with clear, direct answer to the question",
            tools=tools,
            agent=agent,
        )

        # Execute with Crew
        crew = Crew(
            agents=[agent],
            tasks=[task],
            process=Process.sequential,
            knowledge_sources=knowledge_sources,
            verbose=True,
            llm=llm,
        )

        logger.info("Executing database analysis...")
        result = crew.kickoff()

        # Extract the actual result content
        if hasattr(result, "raw"):
            return str(result.raw)
        else:
            return str(result)

    except Exception as e:
        logger.exception(f"Error in postgres analyst: {e}")
        return f"Analysis failed: {str(e)}"

    finally:
        if mcp_server_adapter:
            try:
                mcp_server_adapter.stop()
                logger.info("MCP server connection closed")
            except Exception as e:
                logger.warning(f"Error closing MCP connection: {e}")


# -----------------------------
# FastMCP Tool Registration
# -----------------------------
@mcp.tool(name="postgres-analyst")
def postgres_analyst_tool(question: str, user_id: str = "default") -> str:
    """
    Analyze PostgreSQL database and answer questions using SQL queries.

    Args:
        question: The database question to answer
        user_id: Optional user identifier for tracking

    Returns:
        SQL query results with analysis and insights
    """
    return run_postgres_analyst(question, user_id)


# -----------------------------
# Server startup
# -----------------------------
if __name__ == "__main__":
    logger.info("Starting Postgres Analyst MCP Tool...")
    logger.info("Tool available: postgres-analyst")

    # Run the FastMCP server
    mcp.run(transport="sse", host="127.0.0.1", port=8004)
