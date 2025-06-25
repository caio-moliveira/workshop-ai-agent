import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.graph import StateGraph, MessagesState, START
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_openai import ChatOpenAI


async def main():
    # Initialize the chat model
    model = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    # Configure MCP client with Upstash Context7 server
    client = MultiServerMCPClient(
        {
            "context7": {
                "command": "npx",
                "args": ["-y", "@upstash/context7-mcp@latest"],
                "transport": "stdio",
            }
        }
    )

    try:
        # Get available tools from the MCP server
        tools = await client.get_tools()
        print("Connected to Context7 MCP server!")
        print(f"Available tools: {[tool.name for tool in tools]}\n")

        # Define the model calling function
        def call_model(state: MessagesState):
            response = model.bind_tools(tools).invoke(state["messages"])
            return {"messages": response}

        # Build the graph
        builder = StateGraph(MessagesState)
        builder.add_node("call_model", call_model)
        builder.add_node("tools", ToolNode(tools))

        # Add edges
        builder.add_edge(START, "call_model")
        builder.add_conditional_edges(
            "call_model",
            tools_condition,
        )
        builder.add_edge("tools", "call_model")

        # Compile the graph
        graph = builder.compile()

        # =================================================================
        # 🔍 LANGGRAPH VISUALIZATION & MONITORING FEATURES
        # =================================================================

        print("📊 LangGraph Visualization Features:")
        print("=" * 50)

        # 1. Graph Structure Visualization
        print("1️⃣ Graph Structure:")
        try:
            # Get the Mermaid diagram representation
            mermaid_diagram = graph.get_graph().draw_mermaid()
            print("Mermaid Diagram:")
            print(mermaid_diagram)
            print()
        except Exception as e:
            print(f"Mermaid visualization error: {e}")

        # 2. Graph Nodes and Edges
        print("2️⃣ Graph Analysis:")
        graph_data = graph.get_graph()
        print(f"Nodes: {list(graph_data.nodes.keys())}")
        print(f"Edges: {[(edge.source, edge.target) for edge in graph_data.edges]}")
        print()

        # 3. Stream execution with step-by-step visibility
        print("3️⃣ Step-by-Step Execution Streaming:")
        print("-" * 30)

        test_query = "Find documentation for React hooks"
        print(f"Query: {test_query}")
        print("\nExecution Steps:")

        step_count = 0
        async for event in graph.astream({"messages": [("user", test_query)]}):
            step_count += 1
            print(
                f"Step {step_count}: {list(event.keys())} -> {type(event[list(event.keys())[0]]['messages'][-1])}"
            )

            # Show the actual content for interesting steps
            for node_name, node_output in event.items():
                if node_name == "call_model":
                    last_msg = node_output["messages"][-1]
                    if hasattr(last_msg, "tool_calls") and last_msg.tool_calls:
                        print(
                            f"  🔧 Tool calls: {[tc['name'] for tc in last_msg.tool_calls]}"
                        )
                elif node_name == "tools":
                    print("  📋 Tool execution completed")

        print(f"\nTotal execution steps: {step_count}")
        print()

        # 4. State inspection at each step
        print("4️⃣ Detailed State Tracking:")
        print("-" * 30)

        config = {"configurable": {"thread_id": "test-thread"}}

        # Execute with state tracking
        final_state = await graph.ainvoke(
            {"messages": [("user", "What is FastAPI?")]}, config=config
        )

        print("Final State Messages:")
        for i, msg in enumerate(final_state["messages"]):
            msg_type = type(msg).__name__
            content_preview = (
                str(msg.content)[:100] + "..."
                if len(str(msg.content)) > 100
                else str(msg.content)
            )
            print(f"  Message {i + 1} ({msg_type}): {content_preview}")

        print()

        # 5. Interactive mode with enhanced monitoring
        print("=" * 60)
        print("🚀 Interactive Mode with LangGraph Monitoring")
        print("Commands:")
        print("  - Ask any question")
        print("  - Type 'graph' to see the graph structure")
        print("  - Type 'stream' + question to see step-by-step execution")
        print("  - Type 'quit' to exit")
        print("=" * 60)

        while True:
            user_input = input("\n💬 Your input: ").strip()
            if user_input.lower() in ["quit", "exit", "q"]:
                break

            if user_input.lower() == "graph":
                print("\n📊 Current Graph Structure:")
                try:
                    print(graph.get_graph().draw_mermaid())
                except Exception:
                    print("Graph visualization not available")
                continue

            if user_input.lower().startswith("stream "):
                query = user_input[7:]  # Remove "stream " prefix
                print(f"\n🔄 Streaming execution for: {query}")
                print("-" * 40)

                step = 0
                async for event in graph.astream({"messages": [("user", query)]}):
                    step += 1
                    node_name = list(event.keys())[0]
                    print(f"Step {step}: Executing '{node_name}'")

                    if node_name == "call_model":
                        last_msg = event[node_name]["messages"][-1]
                        if hasattr(last_msg, "tool_calls") and last_msg.tool_calls:
                            print(
                                f"  → Will call tools: {[tc['name'] for tc in last_msg.tool_calls]}"
                            )
                        else:
                            print("  → Generated response (no tools needed)")
                    elif node_name == "tools":
                        print("  → Tools executed successfully")

                print(f"\n✅ Execution completed in {step} steps")
                continue

            if user_input:
                print("\n🤖 Response:")
                response = await graph.ainvoke({"messages": [("user", user_input)]})
                final_message = response["messages"][-1]
                print(final_message.content)

    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Clean up the client connection (if available)
        if hasattr(client, "close"):
            await client.close()
        print("\n👋 Connection cleanup completed")


if __name__ == "__main__":
    asyncio.run(main())
