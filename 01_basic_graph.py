"""
LangGraph Tutorial - Part 1: Basic Graph
=========================================

This tutorial demonstrates the fundamental concepts of LangGraph:
1. Defining a State
2. Creating Nodes
3. Building a Graph with Edges
4. Compiling and Running the Graph
"""

from typing_extensions import TypedDict, Annotated
from langgraph.graph import StateGraph, START, END
import operator


# Step 1: Define the State
# The state is a TypedDict that represents the data flowing through the graph
class State(TypedDict):
    # Annotated with operator.add means values will be accumulated
    messages: Annotated[list[str], operator.add]
    counter: int


# Step 2: Define Node Functions
# Nodes are functions that take state and return state updates
def node_a(state: State) -> dict:
    """Node A adds a message and increments counter"""
    print("Executing Node A")
    return {
        "messages": ["Hello from Node A!"],
        "counter": state.get("counter", 0) + 1
    }


def node_b(state: State) -> dict:
    """Node B adds a message and increments counter"""
    print("Executing Node B")
    return {
        "messages": ["Hello from Node B!"],
        "counter": state.get("counter", 0) + 1
    }


def node_c(state: State) -> dict:
    """Node C adds a message and increments counter"""
    print("Executing Node C")
    return {
        "messages": ["Hello from Node C!"],
        "counter": state.get("counter", 0) + 1
    }


# Step 3: Build the Graph
def build_graph():
    """Create and configure the StateGraph"""
    # Initialize the graph with our State schema
    graph_builder = StateGraph(State)
    
    # Add nodes to the graph
    graph_builder.add_node("node_a", node_a)
    graph_builder.add_node("node_b", node_b)
    graph_builder.add_node("node_c", node_c)
    
    # Define the flow: START -> A -> B -> C -> END
    graph_builder.add_edge(START, "node_a")
    graph_builder.add_edge("node_a", "node_b")
    graph_builder.add_edge("node_b", "node_c")
    graph_builder.add_edge("node_c", END)
    
    # Compile the graph to make it executable
    graph = graph_builder.compile()
    return graph


# Step 4: Run the Graph
if __name__ == "__main__":
    # Build the graph
    graph = build_graph()
    
    # Initial state
    initial_state = {
        "messages": [],
        "counter": 0
    }
    
    # Run the graph
    print("=" * 50)
    print("Running Basic Graph")
    print("=" * 50)
    result = graph.invoke(initial_state)
    
    print("\nFinal State:")
    print(f"Messages: {result['messages']}")
    print(f"Counter: {result['counter']}")
    
    # Visualize the graph
    print("\n" + "=" * 50)
    print("Graph Visualization")
    print("=" * 50)
    try:
        # Get the graph structure
        graph_structure = graph.get_graph()
        
        # Always print Mermaid diagram (works without graphviz)
        mermaid_diagram = graph_structure.draw_mermaid()
        print("\nMermaid Diagram (can be used in Markdown/docs):")
        print("-" * 50)
        print(mermaid_diagram)
        print("-" * 50)
        print("\n💡 Tip: Copy this into Markdown files - GitHub supports Mermaid!")
        
        # Try to save as PNG (optional, requires graphviz)
        try:
            graph_image = graph_structure.draw_mermaid_png()
            with open("graph_visualization.png", "wb") as f:
                f.write(graph_image)
            print("\n✓ PNG image saved as 'graph_visualization.png'")
        except (ImportError, Exception) as png_error:
            print("\n⚠ PNG export not available (graphviz not installed)")
            print("   Mermaid text above works great for documentation!")
            print("   To enable PNG: brew install graphviz && uv pip install pygraphviz")
        
    except Exception as e:
        print(f"⚠ Graph visualization error: {e}")
        print("\nThis is unusual - basic Mermaid text should always work.")
