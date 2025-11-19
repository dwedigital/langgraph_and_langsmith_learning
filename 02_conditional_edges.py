"""
LangGraph Tutorial - Part 2: Conditional Edges
===============================================

This tutorial demonstrates conditional routing in LangGraph:
1. Conditional edges that route based on state
2. Dynamic decision making in the graph
"""

from typing_extensions import TypedDict, Annotated
from langgraph.graph import StateGraph, START, END
import operator


# Define State with a routing field
class State(TypedDict):
    messages: Annotated[list[str], operator.add]
    route: str  # Determines which path to take
    value: int


# Node functions
def start_node(state: State) -> dict:
    """Start node that sets up routing"""
    print("Executing Start Node")
    return {
        "messages": ["Starting..."],
        "route": state.get("route", "path_b"),  # Change this to "path_b" or "path_c" to see different paths
        "value": 10
    }


def path_b_node(state: State) -> dict:
    """Path B: multiplies value by 2"""
    print("Executing Path B (multiply by 2)")
    return {
        "messages": [f"Path B: {state['value']} * 2 = {state['value'] * 2}"],
        "value": state['value'] * 2
    }


def path_c_node(state: State) -> dict:
    """Path C: adds 5 to value"""
    print("Executing Path C (add 5)")
    return {
        "messages": [f"Path C: {state['value']} + 5 = {state['value'] + 5}"],
        "value": state['value'] + 5
    }


def final_node(state: State) -> dict:
    """Final node that processes the result"""
    print("Executing Final Node")
    return {
        "messages": [f"Final value: {state['value']}"]
    }


# Conditional routing function
def route_decision(state: State) -> str:
    """
    This function determines which node to go to next.
    It must return a string matching one of the node names.
    """
    route = state.get("route")
    print(f"State: {state}")
    print(f"Routing decision: {route}")
    return route


def build_graph():
    """Create graph with conditional edges"""
    graph_builder = StateGraph(State)
    
    # Add all nodes
    graph_builder.add_node("start", start_node)
    graph_builder.add_node("path_b", path_b_node)
    graph_builder.add_node("path_c", path_c_node)
    graph_builder.add_node("final", final_node)
    
    # Start from START node
    graph_builder.add_edge(START, "start")
    
    # Conditional edge: start -> (path_b OR path_c) based on route_decision
    graph_builder.add_conditional_edges(
        "start",
        route_decision,  # Function that returns the next node name
        {
            "path_b": "path_b",  # Maps return value to node
            "path_c": "path_c"
        }
    )
    
    # Both paths lead to final node
    graph_builder.add_edge("path_b", "final")
    graph_builder.add_edge("path_c", "final")
    graph_builder.add_edge("final", END)
    
    return graph_builder.compile()


if __name__ == "__main__":
    graph = build_graph()
    
    # Test with route to path_b
    print("=" * 50)
    print("Test 1: Routing to Path B")
    print("=" * 50)
    initial_state = {
        "messages": [],
        "route": "path_b",
        "value": 10
    }
    result = graph.invoke(initial_state)
    print(f"\nFinal Messages: {result['messages']}")
    print(f"Final Value: {result['value']}")
    
    # Test with route to path_c
    print("\n" + "=" * 50)
    print("Test 2: Routing to Path C")
    print("=" * 50)
    initial_state = {
        "messages": [],
        "route": "path_c",
        "value": 10
    }
    result = graph.invoke(initial_state)
    print(f"\nFinal Messages: {result['messages']}")
    print(f"Final Value: {result['value']}")
