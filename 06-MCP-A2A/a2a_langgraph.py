"""
Simple Agent-to-Agent (A2A) Example using LangGraph with LLMs
This example demonstrates two LLM-powered agents collaborating: a Researcher and a Writer
"""

from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.tools.tavily_search import TavilySearchResults
import operator
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file


# Define the state that will be passed between agents
class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    research_complete: bool
    topic: str
    research_findings: str
    final_article: str


# Initialize LLM (you can use different models for different agents)
def get_llm(model="gpt-3.5-turbo", temperature=0.7):
    """Get LLM instance - replace with your preferred model"""
    return ChatOpenAI(
        model=model,
        temperature=temperature,
        api_key=os.getenv("OPENAI_API_KEY"),  # Make sure to set your API key
    )


# Researcher Agent with Tavily and LLM
def researcher_agent(state: AgentState):
    """
    LLM-powered researcher agent that uses Tavily for web search and LLM for analysis
    """
    topic = state["topic"]
    llm = get_llm(temperature=0.3)  # Lower temperature for more focused research

    # Initialize Tavily search tool
    tavily_tool = TavilySearchResults(
        max_results=5,
        search_depth="advanced",
        include_answer=True,
        include_raw_content=False,
        include_images=False,
        api_key=os.getenv("TAVILY_API_KEY"),  # Make sure to set your Tavily API key
    )

    try:
        # Step 1: Use Tavily to search for current information
        print(f"🔍 Searching the web for: {topic}")
        search_results = tavily_tool.invoke({"query": topic})

        # Extract search information
        search_content = ""
        for result in search_results:
            search_content += f"Source: {result.get('url', 'N/A')}\n"
            search_content += f"Title: {result.get('title', 'N/A')}\n"
            search_content += f"Content: {result.get('content', 'N/A')}\n\n"

        # Step 2: Use LLM to analyze and synthesize the search results
        analysis_prompt = ChatPromptTemplate.from_messages(
            [
                SystemMessage(
                    content="""You are a research analyst. Your job is to analyze web search results and create comprehensive research findings.
            
            Based on the search results provided, create structured research findings that include:
            - Key concepts and definitions
            - Current trends and developments  
            - Benefits and challenges
            - Best practices and recommendations
            - Relevant statistics or data points
            - Recent news or updates
            
            Synthesize the information from multiple sources and present it in a clear, organized format.
            Always cite or reference the sources when mentioning specific information."""
                ),
                HumanMessage(
                    content=f"""Please analyze these web search results about '{topic}' and create comprehensive research findings:

Search Results:
{search_content}

Topic: {topic}"""
                ),
            ]
        )

        # Get analysis from LLM
        analysis_chain = analysis_prompt | llm
        analysis_response = analysis_chain.invoke(
            {"topic": topic, "search_content": search_content}
        )

        research_findings = analysis_response.content

    except Exception as e:
        print(f"⚠️ Error with Tavily search: {e}")
        print("🔄 Falling back to LLM-only research...")

        # Fallback to LLM-only research if Tavily fails
        fallback_prompt = ChatPromptTemplate.from_messages(
            [
                SystemMessage(
                    content="""You are a research specialist. Your job is to provide comprehensive information about a given topic based on your knowledge.
            Note: This research is based on your training data and may not include the very latest developments.
            
            Provide detailed research findings including:
            - Key concepts and definitions
            - Current trends and developments
            - Benefits and challenges  
            - Best practices and recommendations
            - Relevant information from your knowledge base
            
            Format your response as structured research findings."""
                ),
                HumanMessage(content=f"Please research the topic: {topic}"),
            ]
        )

        fallback_chain = fallback_prompt | llm
        fallback_response = fallback_chain.invoke({"topic": topic})
        research_findings = fallback_response.content

    # Update state with research findings
    return {
        "messages": [
            AIMessage(
                content=f"Research completed for topic: {topic} using web search and analysis"
            )
        ],
        "research_complete": True,
        "research_findings": research_findings,
    }


# Writer Agent with LLM
def writer_agent(state: AgentState):
    """
    LLM-powered writer agent that creates an article based on research findings
    """
    topic = state["topic"]
    research = state["research_findings"]
    llm = get_llm(temperature=0.8)  # Higher temperature for more creative writing

    # Create writing prompt
    writing_prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessage(
                content="""You are a professional technical writer. Your job is to create well-structured, engaging articles based on research findings.
        
        Create an article that includes:
        - Compelling introduction
        - Clear sections with headers
        - Integration of research findings
        - Practical insights and takeaways
        - Professional conclusion
        
        Make the article informative yet accessible to a general audience."""
            ),
            HumanMessage(
                content=f"""Please write a comprehensive article about '{topic}' based on these research findings:

{research}

Create a well-structured article that incorporates this research effectively."""
            ),
        ]
    )

    # Get article from LLM
    writing_chain = writing_prompt | llm
    article_response = writing_chain.invoke({"topic": topic, "research": research})

    article = article_response.content

    return {
        "messages": [AIMessage(content=f"Article completed for topic: {topic}")],
        "final_article": article,
    }


# Coordinator function to determine next steps
def should_continue(state: AgentState):
    """
    Determine if research is complete and writing can begin
    """
    if state.get("research_complete", False):
        return "writer"
    else:
        return "researcher"


# Create the graph
def create_a2a_workflow():
    """
    Create a simple A2A workflow with LangGraph and LLM-powered agents
    """
    # Initialize the state graph
    workflow = StateGraph(AgentState)

    # Add agent nodes
    workflow.add_node("researcher", researcher_agent)
    workflow.add_node("writer", writer_agent)

    # Add edges
    workflow.add_edge(START, "researcher")
    workflow.add_conditional_edges(
        "researcher", should_continue, {"writer": "writer", "researcher": "researcher"}
    )
    workflow.add_edge("writer", END)

    # Compile the graph
    app = workflow.compile()
    return app


# Example usage
def run_a2a_example():
    """
    Run the LLM-powered A2A example workflow
    """
    # Check if API keys are set
    missing_keys = []
    if not os.getenv("OPENAI_API_KEY"):
        missing_keys.append("OPENAI_API_KEY")
    if not os.getenv("TAVILY_API_KEY"):
        missing_keys.append("TAVILY_API_KEY")

    if missing_keys:
        print("⚠️  Please set the following environment variables:")
        for key in missing_keys:
            print(f"   export {key}='your-key-here'")
        print("\n📝 Note: You can get a Tavily API key at https://tavily.com")
        print("   Tavily provides web search capabilities for AI agents")
        return

    # Create the workflow
    app = create_a2a_workflow()

    # Define initial state
    initial_state = {
        "messages": [HumanMessage(content="Please research and write about AI agents")],
        "research_complete": False,
        "topic": "Jornada de Dados",
        "research_findings": "",
        "final_article": "",
    }

    # Run the workflow
    print("🚀 Starting LLM-Powered A2A Workflow...")
    print("=" * 50)
    print("🔍 Researcher Agent is gathering information...")

    result = app.invoke(initial_state)

    # Display results
    print("\n📊 Research Findings:")
    print("-" * 30)
    print(result["research_findings"])
    print("\n" + "=" * 50)

    print("📝 Final Article:")
    print("-" * 30)
    print(result["final_article"])
    print("\n" + "=" * 50)

    print("✅ LLM-Powered A2A Workflow Completed!")
    print(f"Messages exchanged: {len(result['messages'])}")

    return result


if __name__ == "__main__":
    # Run the example
    result = run_a2a_example()
