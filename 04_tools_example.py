"""
LangGraph Tutorial - Part 4: Graph with Tools
==============================================

This tutorial demonstrates:
1. Adding tools to a graph
2. Conditional routing based on tool calls
3. Tool execution node
"""

from typing_extensions import TypedDict, Annotated
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage, ToolMessage
from langchain_core.tools import tool
import operator


# Define tools
@tool
def calculator(expression: str) -> str:
    """Evaluate a mathematical expression. Input should be a valid Python expression."""
    try:
        result = eval(expression)
        return f"Result: {result}"
    except Exception as e:
        return f"Error: {str(e)}"


@tool
def get_weather(city: str) -> str:
    """Get the weather for a city. Returns mock weather data."""
    # In production, this would call a real weather API
    return f"The weather in {city} is sunny, 72°F"


# Create list of tools
tools = [calculator, get_weather]


# State for the agent
class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], operator.add]


def chatbot_node(state: AgentState) -> dict:
    """
    Simple chatbot that decides whether to use tools.
    In production, this would use an LLM with tool binding.
    """
    messages = state["messages"]
    last_message = messages[-1]

    if isinstance(last_message, HumanMessage):
        content = last_message.content.lower()

        # Simple rule-based routing (in production, LLM decides)
        if (
            "calculate" in content
            or "math" in content
            or "+" in content
            or "*" in content
        ):
            # Extract expression (simplified - in production, LLM would do this)
            expression = content.replace("calculate", "").replace("math", "").strip()
            # Create tool call
            tool_message = AIMessage(
                content="",
                tool_calls=[
                    {
                        "name": "calculator",
                        "args": {"expression": expression},
                        "id": "1",
                    }
                ],
            )
            return {"messages": [tool_message]}

        elif "weather" in content:
            # Extract city (simplified)
            city = "San Francisco"  # Default
            if "in" in content:
                parts = content.split("in")
                if len(parts) > 1:
                    city = parts[-1].strip()

            tool_message = AIMessage(
                content="",
                tool_calls=[{"name": "get_weather", "args": {"city": city}, "id": "2"}],
            )
            return {"messages": [tool_message]}

        else:
            # Regular response
            response = f"I can help with calculations and weather. You said: {last_message.content}"
            return {"messages": [AIMessage(content=response)]}

    return {}


def should_continue(state: AgentState) -> str:
    """Determine if we should continue to tools or end"""
    messages = state["messages"]
    last_message = messages[-1]

    # If last message has tool calls, go to tools
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"

    # Otherwise, end
    return END


def build_agent_graph():
    """Build an agent graph with tools"""
    graph_builder = StateGraph(AgentState)

    # Add nodes
    graph_builder.add_node("chatbot", chatbot_node)
    graph_builder.add_node("tools", ToolNode(tools))

    # Define flow
    graph_builder.add_edge(START, "chatbot")

    # Conditional edge: chatbot -> tools OR END
    graph_builder.add_conditional_edges(
        "chatbot", should_continue, {"tools": "tools", END: END}
    )

    # Tools always go back to chatbot
    graph_builder.add_edge("tools", "chatbot")

    return graph_builder.compile()


if __name__ == "__main__":
    graph = build_agent_graph()

    print("=" * 50)
    print("LangGraph Agent with Tools")
    print("=" * 50)

    # Test 1: Regular message
    print("\n--- Test 1: Regular Message ---")
    state = {"messages": [HumanMessage(content="Hello!")]}
    result = graph.invoke(state)
    print(f"User: {state['messages'][0].content}")
    print(f"Assistant: {result['messages'][-1].content}")

    # Test 2: Math calculation
    print("\n--- Test 2: Math Calculation ---")
    state = {"messages": [HumanMessage(content="Calculate 15 * 7 + 3")]}
    result = graph.invoke(state)
    print(f"User: {state['messages'][0].content}")
    # Find the tool result
    for msg in result["messages"]:
        if isinstance(msg, ToolMessage):
            print(f"Tool Result: {msg.content}")
        elif isinstance(msg, AIMessage) and msg.content:
            print(f"Assistant: {msg.content}")

    # Test 3: Weather query
    print("\n--- Test 3: Weather Query ---")
    state = {"messages": [HumanMessage(content="What's the weather in New York?")]}
    result = graph.invoke(state)
    print(f"User: {state['messages'][0].content}")
    for msg in result["messages"]:
        if isinstance(msg, ToolMessage):
            print(f"Tool Result: {msg.content}")
        elif isinstance(msg, AIMessage) and msg.content:
            print(f"Assistant: {msg.content}")
