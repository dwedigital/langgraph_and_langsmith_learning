"""
LangGraph Tutorial - Part 6: LangSmith Observability
======================================================

This tutorial demonstrates how to integrate LangSmith for observability
and tracing in LangGraph applications.

LangSmith provides:
- Real-time tracing of graph execution
- Performance monitoring
- Debugging and error tracking
- Cost tracking
- Conversation analytics
"""

from typing_extensions import TypedDict, Annotated
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from langchain_core.tracers.context import tracing_v2_enabled
from langsmith import Client
import operator
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


# State for the chatbot
class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], operator.add]
    turn_count: int


def setup_langsmith():
    """
    Configure LangSmith tracing.
    
    Required environment variables:
    - LANGSMITH_API_KEY: Your LangSmith API key
    - LANGCHAIN_PROJECT: Project name (optional, defaults to 'default')
    """
    # Check if LangSmith is configured
    api_key = os.getenv("LANGSMITH_API_KEY")
    
    if not api_key:
        print("⚠️  LangSmith API key not found!")
        print("   Set LANGSMITH_API_KEY or LANGCHAIN_API_KEY in your .env file")
        print("   Get your API key from: https://smith.langchain.com/")
        return None
    
    # Enable tracing
    os.environ["LANGSMITH_TRACING"] = "true"
    os.environ["LANGSMITH_ENDPOINT"] = os.getenv(
        "LANGSMITH_ENDPOINT", 
        "https://api.smith.langchain.com"
    )
    os.environ["LANGCHAIN_PROJECT"] = os.getenv(
        "LANGSMITH_PROJECT",
        "langraph-tutorial"
    )
    
    # Create LangSmith client
    client = Client(
        api_key=api_key,
        api_url=os.getenv("LANGSMITH_ENDPOINT", "https://api.smith.langchain.com")
    )
    
    print("✅ LangSmith tracing enabled")
    print(f"   Project: {os.environ['LANGCHAIN_PROJECT']}")
    print(f"   View traces at: https://smith.langchain.com/")
    
    return client


def chatbot_node(state: ChatState) -> dict:
    """
    Simple chatbot node that processes messages.
    In production, this would call an LLM.
    """
    messages = state["messages"]
    last_message = messages[-1]
    
    if isinstance(last_message, HumanMessage):
        # Simulate LLM processing
        response = f"Echo: {last_message.content}"
        print(f"Chatbot processing: {last_message.content}")
        return {
            "messages": [AIMessage(content=response)],
            "turn_count": state.get("turn_count", 0) + 1
        }
    return {}


def build_chatbot_graph():
    """Build a simple chatbot graph"""
    graph_builder = StateGraph(ChatState)
    
    graph_builder.add_node("chatbot", chatbot_node)
    graph_builder.add_edge(START, "chatbot")
    graph_builder.add_edge("chatbot", END)
    
    return graph_builder.compile()


def build_llm_chatbot_graph():
    """
    Build a chatbot graph with actual LLM and LangSmith tracing.
    This will automatically trace all LLM calls.
    """
    try:
        from langchain_ollama import ChatOllama
        
        # Initialize Ollama LLM with Llama 3.1
        llm = ChatOllama(
            model="llama3.1",
            temperature=0,
            base_url="http://localhost:11434"  # Default Ollama URL
        )
        
        def llm_chatbot_node(state: ChatState) -> dict:
            """Chatbot node that uses an actual LLM (traced by LangSmith)"""
            messages = state["messages"]
            print(f"LLM processing {len(messages)} messages")
            
            # This LLM call will be automatically traced
            response = llm.invoke(messages)
            return {
                "messages": [response],
                "turn_count": state.get("turn_count", 0) + 1
            }
        
        graph_builder = StateGraph(ChatState)
        graph_builder.add_node("chatbot", llm_chatbot_node)
        graph_builder.add_edge(START, "chatbot")
        graph_builder.add_edge("chatbot", END)
        
        return graph_builder.compile()
    except Exception as e:
        print(f"Could not initialize LLM: {e}")
        print("Falling back to echo chatbot")
        return build_chatbot_graph()


def example_basic_tracing():
    """Example 1: Basic tracing with environment variables"""
    print("=" * 60)
    print("Example 1: Basic LangSmith Tracing")
    print("=" * 60)
    
    # Setup LangSmith
    client = setup_langsmith()
    
    if not client:
        print("\n⚠️  Skipping tracing example - API key not configured")
        return
    
    # Build and run graph
    graph = build_chatbot_graph()
    
    # Run with tracing enabled
    # Traces are automatically sent to LangSmith
    with tracing_v2_enabled(client=client):
        state = {
            "messages": [HumanMessage(content="Hello! What is LangGraph?")],
            "turn_count": 0
        }
        result = graph.invoke(state)
        
        print(f"\nUser: {state['messages'][0].content}")
        print(f"Assistant: {result['messages'][-1].content}")
        print(f"Turns: {result['turn_count']}")
    
    print("\n✅ Check your LangSmith dashboard to see the trace!")


def example_custom_trace_metadata():
    """Example 2: Adding custom metadata to traces"""
    print("\n" + "=" * 60)
    print("Example 2: Custom Trace Metadata")
    print("=" * 60)
    
    client = setup_langsmith()
    
    if not client:
        print("\n⚠️  Skipping tracing example - API key not configured")
        return
    
    graph = build_chatbot_graph()
    
    # Add custom metadata to the trace
    config = {
        "run_name": "custom-chatbot-run",
        "tags": ["tutorial", "observability", "demo"],
        "metadata": {
            "user_id": "user_123",
            "session_id": "session_456",
            "version": "1.0.0"
        }
    }
    
    with tracing_v2_enabled(client=client):
        state = {
            "messages": [HumanMessage(content="Tell me about observability")],
            "turn_count": 0
        }
        result = graph.invoke(state, config)
        
        print(f"\nUser: {state['messages'][0].content}")
        print(f"Assistant: {result['messages'][-1].content}")
        print(f"Run name: {config['run_name']}")
        print(f"Tags: {config['tags']}")
    
    print("\n✅ Check LangSmith for trace with custom metadata!")


def example_llm_tracing():
    """Example 3: Tracing LLM calls (requires API key)"""
    print("\n" + "=" * 60)
    print("Example 3: LLM Call Tracing")
    print("=" * 60)
    
    client = setup_langsmith()
    
    if not client:
        print("\n⚠️  Skipping LLM tracing - API key not configured")
        return
    
    # Check if we have an LLM API key
    has_openai_key = os.getenv("OPENAI_API_KEY") or os.getenv("ANTHROPIC_API_KEY")
    
    if not has_openai_key:
        print("\n⚠️  No LLM API key found (OPENAI_API_KEY or ANTHROPIC_API_KEY)")
        print("   LLM calls won't work, but tracing setup is shown")
        return
    
    graph = build_llm_chatbot_graph()
    
    config = {
        "run_name": "llm-chatbot-trace",
        "tags": ["llm", "gpt-4o-mini"]
    }
    
    with tracing_v2_enabled(client=client):
        state = {
            "messages": [HumanMessage(content="What is observability in AI?")],
            "turn_count": 0
        }
        result = graph.invoke(state, config)
        
        print(f"\nUser: {state['messages'][0].content}")
        print(f"Assistant: {result['messages'][-1].content}")
    
    print("\n✅ Check LangSmith to see detailed LLM call traces!")
    print("   You'll see token usage, latency, and response details")


def example_streaming_with_tracing():
    """Example 4: Streaming with tracing"""
    print("\n" + "=" * 60)
    print("Example 4: Streaming with Tracing")
    print("=" * 60)
    
    client = setup_langsmith()
    
    if not client:
        print("\n⚠️  Skipping streaming example - API key not configured")
        return
    
    graph = build_chatbot_graph()
    
    config = {
        "run_name": "streaming-chatbot",
        "tags": ["streaming"]
    }
    
    with tracing_v2_enabled(client=client):
        state = {
            "messages": [HumanMessage(content="Count to 3")],
            "turn_count": 0
        }
        
        print("\nStreaming execution:")
        for event in graph.stream(state, config, stream_mode="values"):
            if "messages" in event:
                last_msg = event["messages"][-1]
                if isinstance(last_msg, AIMessage):
                    print(f"  → {last_msg.content}")
            if "turn_count" in event:
                print(f"  → Turn count: {event['turn_count']}")
    
    print("\n✅ Streamed execution traced in LangSmith!")


if __name__ == "__main__":
    print("LangGraph + LangSmith Observability Tutorial")
    print("=" * 60)
    print("\nThis tutorial demonstrates LangSmith integration for:")
    print("  • Automatic tracing of graph execution")
    print("  • LLM call monitoring")
    print("  • Performance metrics")
    print("  • Debugging and error tracking")
    print("\n" + "=" * 60)
    
    # Run examples
    example_basic_tracing()
    example_custom_trace_metadata()
    example_llm_tracing()
    example_streaming_with_tracing()
    
    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    print("""
LangSmith Integration Benefits:

1. Automatic Tracing
   - All graph nodes are automatically traced
   - LLM calls are captured with full details
   - Tool executions are logged

2. Observability
   - View execution flow in real-time
   - See performance metrics (latency, tokens)
   - Track costs per run

3. Debugging
   - Inspect inputs/outputs at each step
   - Identify bottlenecks
   - Debug errors with full context

4. Analytics
   - Track conversation patterns
   - Monitor usage over time
   - Set up alerts

Next Steps:
- Visit https://smith.langchain.com/ to view your traces
- Set up alerts for errors or high latency
- Use datasets to test and evaluate your graphs
- Export traces for analysis

Environment Variables:
- LANGSMITH_API_KEY: Your API key (required)
- LANGCHAIN_PROJECT: Project name (optional)
- LANGCHAIN_ENDPOINT: API endpoint (optional, defaults to smith.langchain.com)
    """)

