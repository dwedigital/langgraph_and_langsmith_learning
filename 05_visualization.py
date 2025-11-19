"""
LangGraph Tutorial - Part 5: Graph Visualization
=================================================

This tutorial demonstrates different ways to visualize LangGraph workflows:
1. Mermaid diagrams (text format)
2. PNG images (requires graphviz system library)
3. ASCII art visualization
4. Exporting for documentation
"""

from typing_extensions import TypedDict, Annotated
from langgraph.graph import StateGraph, START, END
import operator


# Define a sample state for demonstration
class State(TypedDict):
    messages: Annotated[list[str], operator.add]
    counter: int
    route: str


# Sample nodes
def node_a(state: State) -> dict:
    return {"messages": ["A"], "counter": state.get("counter", 0) + 1}


def node_b(state: State) -> dict:
    return {"messages": ["B"], "counter": state.get("counter", 0) + 1}


def node_c(state: State) -> dict:
    return {"messages": ["C"], "counter": state.get("counter", 0) + 1}


def route_decision(state: State) -> str:
    return state.get("route", "node_b")


def build_example_graph():
    """Build a graph with conditional edges for visualization"""
    graph_builder = StateGraph(State)

    graph_builder.add_node("node_a", node_a)
    graph_builder.add_node("node_b", node_b)
    graph_builder.add_node("node_c", node_c)

    graph_builder.add_edge(START, "node_a")
    graph_builder.add_conditional_edges(
        "node_a", route_decision, {"node_b": "node_b", "node_c": "node_c"}
    )
    graph_builder.add_edge("node_b", END)
    graph_builder.add_edge("node_c", END)

    return graph_builder.compile()


def visualize_mermaid_text(graph):
    """Method 1: Get Mermaid diagram as text"""
    print("=" * 60)
    print("Method 1: Mermaid Diagram (Text Format)")
    print("=" * 60)
    try:
        graph_structure = graph.get_graph()
        mermaid_diagram = graph_structure.draw_mermaid()
        print(mermaid_diagram)
        print("\n💡 Tip: You can copy this into Markdown files or Mermaid editors")
        print("   Example: https://mermaid.live/")
        return mermaid_diagram
    except Exception as e:
        print(f"Error: {e}")
        return None


def visualize_png_image(graph, filename="graph.png"):
    """Method 2: Save as PNG image (requires system graphviz)"""
    print("\n" + "=" * 60)
    print("Method 2: PNG Image Export")
    print("=" * 60)
    try:
        graph_structure = graph.get_graph()
        graph_image = graph_structure.draw_mermaid_png()

        with open(filename, "wb") as f:
            f.write(graph_image)

        print(f"✓ Successfully saved graph as '{filename}'")
        print(f"  File size: {len(graph_image)} bytes")
        return True
    except ImportError as e:
        print("⚠ PNG export requires pygraphviz package")
        print(f"  Error: {e}")
        print("\nTo enable PNG export:")
        print("  1. Install system graphviz:")
        print("     macOS:   brew install graphviz")
        print("     Linux:   sudo apt-get install graphviz graphviz-dev")
        print("     Windows: https://graphviz.org/download/")
        print("  2. Then install Python package:")
        print("     uv pip install pygraphviz")
        print("\n💡 Tip: Mermaid text format (Method 1) works without graphviz!")
        return False
    except Exception as e:
        error_msg = str(e).lower()
        if "graphviz" in error_msg or "dot" in error_msg or "not found" in error_msg:
            print("⚠ System graphviz library not found")
            print(f"  Error: {e}")
            print("\nTo fix this:")
            print("  1. Install system graphviz:")
            print("     macOS:   brew install graphviz")
            print("     Linux:   sudo apt-get install graphviz graphviz-dev")
            print("     Windows: https://graphviz.org/download/")
            print("  2. Verify installation: dot -V")
            print("  3. If needed, install Python package: uv pip install pygraphviz")
        else:
            print(f"⚠ Failed to create PNG: {e}")
            print("\nThis might be a graphviz configuration issue.")
            print("Try installing system graphviz first (see above).")
        print("\n💡 Tip: Mermaid text format (Method 1) works without graphviz!")
        return False


def visualize_ascii(graph):
    """Method 3: ASCII art representation"""
    print("\n" + "=" * 60)
    print("Method 3: ASCII Art Visualization")
    print("=" * 60)
    try:
        graph_structure = graph.get_graph()
        ascii_art = graph_structure.draw_ascii()
        print(ascii_art)
        return ascii_art
    except Exception as e:
        print(f"⚠ ASCII visualization not available: {e}")
        return None


def save_mermaid_to_file(graph, filename="graph.mmd"):
    """Save Mermaid diagram to a file for documentation"""
    print("\n" + "=" * 60)
    print("Method 4: Save Mermaid to File")
    print("=" * 60)
    try:
        graph_structure = graph.get_graph()
        mermaid_diagram = graph_structure.draw_mermaid()

        with open(filename, "w") as f:
            f.write(mermaid_diagram)

        print(f"✓ Saved Mermaid diagram to '{filename}'")
        print("  You can use this in:")
        print("  - GitHub README.md (Mermaid is supported)")
        print("  - Documentation sites")
        print("  - Mermaid Live Editor (https://mermaid.live/)")
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False


def print_graph_info(graph):
    """Print information about the graph structure"""
    print("\n" + "=" * 60)
    print("Graph Information")
    print("=" * 60)
    try:
        graph_structure = graph.get_graph()

        # Get nodes
        nodes = graph_structure.nodes
        print(f"\nNodes ({len(nodes)}):")
        for node_id in nodes:
            print(f"  - {node_id}")

        # Get edges
        edges = graph_structure.edges
        print(f"\nEdges ({len(edges)}):")
        for edge in edges:
            source = edge.source if hasattr(edge, "source") else "?"
            target = edge.target if hasattr(edge, "target") else "?"
            print(f"  - {source} → {target}")

    except Exception as e:
        print(f"Error getting graph info: {e}")


if __name__ == "__main__":
    # Build the example graph
    graph = build_example_graph()

    print("LangGraph Visualization Tutorial")
    print("=" * 60)
    print("\nThis script demonstrates multiple ways to visualize your LangGraph.")
    print("Choose the method that works best for your needs.\n")

    # Method 1: Mermaid text (always works)
    mermaid_text = visualize_mermaid_text(graph)

    # Method 2: PNG image (requires system graphviz)
    visualize_png_image(graph, "example_graph.png")

    # Method 3: ASCII art
    visualize_ascii(graph)

    # Method 4: Save Mermaid to file
    save_mermaid_to_file(graph, "example_graph.mmd")

    # Print graph structure info
    print_graph_info(graph)

    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    print("""
Visualization Options:
1. Mermaid Text: Always available, great for documentation
2. PNG Image: Requires system graphviz, best for presentations
3. ASCII Art: Simple text representation
4. Mermaid File: Save for use in Markdown/docs

For most use cases, the Mermaid text format is sufficient and
can be embedded directly in Markdown files (GitHub supports it).
    """)
