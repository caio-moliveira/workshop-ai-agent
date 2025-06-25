import os
import logging
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse
from fastmcp import FastMCP
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from crewai import Agent, Task, Crew, Process
from crewai_tools import MCPServerAdapter
from mcp import StdioServerParameters
from crewai.knowledge.source.crew_docling_source import CrewDoclingSource
from crewai.knowledge.storage.knowledge_storage import KnowledgeStorage

from typing import Iterator

# -----------------------------
# Setup logging & environment
# -----------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
load_dotenv()


# -----------------------------
# Request Models
# -----------------------------
class ChatMessage(BaseModel):
    message: str
    agentType: str = "postgres-analyst"


# -----------------------------
# Initialize FastMCP instance
# -----------------------------
fastmcp_instance = FastMCP("postgres-analyst")

# -----------------------------
# Create parent FastAPI app
# -----------------------------
app = FastAPI(title="Postgres Analyst MCP Server", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

# -----------------------------
# Configuration
# -----------------------------
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://caio:4pYLWgRPVeC0GzfOZq7eAYKE6nWAMoLa@dpg-d0m6njbuibrs7386ajh0-a.oregon-postgres.render.com:5432/dbteachable?sslmode=require",
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
@fastmcp_instance.tool(name="postgres-analyst")
def postgres_analyst_tool(question: str, user_id: str = "default") -> str:
    """MCP tool wrapper for the postgres analyst."""
    return run_postgres_analyst(question, user_id)


# -----------------------------
# API Endpoints
# -----------------------------
@app.get("/mcp/")
async def health_check():
    """Health check endpoint."""
    return JSONResponse(
        {"status": "healthy", "service": "postgres-analyst-mcp", "version": "1.0.0"}
    )


@app.post("/mcp/")
async def chat_endpoint(request: ChatMessage):
    """Main chat endpoint for database queries."""
    try:
        logger.info(f"Processing query: {request.message[:100]}...")

        # Run the analysis
        result = run_postgres_analyst(request.message, "web_user")

        # Stream the response
        def generate_response() -> Iterator[str]:
            yield result

        return StreamingResponse(
            generate_response(),
            media_type="text/plain",
            headers={"Cache-Control": "no-cache"},
        )

    except Exception as e:
        logger.exception(f"Chat endpoint error: {e}")
        raise HTTPException(status_code=500, detail=f"Query failed: {str(e)}")


@app.get("/mcp/test")
async def test_connection():
    """Test endpoint to verify MCP connection."""
    try:
        result = run_postgres_analyst("SELECT version();", "test_user")
        return JSONResponse(
            {
                "status": "success",
                "connection": "verified",
                "result": result[:200] + "..." if len(result) > 200 else result,
            }
        )
    except Exception as e:
        return JSONResponse({"status": "error", "message": str(e)}, status_code=500)


# -----------------------------
# Mount FastMCP to main app
# -----------------------------
app.mount("/fastmcp", fastmcp_instance.app)

# -----------------------------
# Server startup
# -----------------------------
if __name__ == "__main__":
    logger.info("Starting Postgres Analyst MCP Server...")
    logger.info("Endpoints:")
    logger.info("  - Health: GET http://127.0.0.1:8004/mcp/")
    logger.info("  - Chat: POST http://127.0.0.1:8004/mcp/")
    logger.info("  - Test: GET http://127.0.0.1:8004/mcp/test")
    logger.info("  - FastMCP: http://127.0.0.1:8004/fastmcp/")

    uvicorn.run(
        "src.mcp_server_db:app",
        host="127.0.0.1",
        port=8004,
        reload=True,
        log_level="info",
    )
