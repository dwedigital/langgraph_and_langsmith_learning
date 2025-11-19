# LangGraph Tutorial

This repository contains a comprehensive tutorial on using LangGraph, a framework for building stateful, multi-agent applications with LLMs.

## What is LangGraph?

LangGraph is a low-level orchestration framework for building, managing, and deploying long-running, stateful agents. It provides:
- **Durable execution**: Persist and resume agent workflows
- **Comprehensive memory**: Built-in state management
- **Human-in-the-loop**: Interrupt and modify agent behavior
- **Production-ready deployment**: Deploy agents as APIs

## Core Concepts

### 1. State
The state is a TypedDict that represents data flowing through the graph. It can contain:
- Messages (for chatbots)
- Variables (for computation)
- Any custom data your application needs

### 2. Nodes
Nodes are functions that:
- Take the current state as input
- Return state updates (partial state)
- Can perform any computation (LLM calls, tool calls, etc.)

### 3. Edges
Edges define the flow between nodes:
- **Regular edges**: Always go to the same next node
- **Conditional edges**: Route based on state or function output
- **START/END**: Special nodes for entry/exit points

### 4. Graph
The graph is compiled from nodes and edges, creating an executable workflow.

## Tutorial Files

### 01_basic_graph.py
**Concepts**: State, Nodes, Edges, Graph compilation

This is the simplest example showing:
- How to define a state schema
- How to create nodes
- How to connect nodes with edges
- How to run a graph

**Run it:**
```bash
# Using uv (recommended)
uv run python 01_basic_graph.py

# Or activate the environment first
uv sync
source .venv/bin/activate  # macOS/Linux
python 01_basic_graph.py
```

### 02_conditional_edges.py
**Concepts**: Conditional routing, Dynamic flow

Demonstrates:
- How to use conditional edges
- How to route based on state
- How to create branching workflows

**Run it:**
```bash
uv run python 02_conditional_edges.py
```

### 03_chatbot_example.py
**Concepts**: Message handling, LLM integration

Shows:
- How to build a simple chatbot
- How to handle conversation state
- How to integrate with LLMs (optional)

**Run it:**
```bash
# With Ollama running (uses Llama 3.1)
# Make sure Ollama is running: ollama serve
# And model is installed: ollama pull llama3.1
uv run python 03_chatbot_example.py

# Without Ollama (uses echo bot)
uv run python 03_chatbot_example.py
```

### 04_tools_example.py
**Concepts**: Tools, Tool execution, Conditional tool routing

Demonstrates:
- How to define and use tools
- How to route to tool execution
- How to handle tool results

**Run it:**
```bash
uv run python 04_tools_example.py
```

### 05_visualization.py
**Concepts**: Graph visualization, Mermaid diagrams, PNG export

Demonstrates:
- How to visualize graphs as Mermaid diagrams
- How to export graphs as PNG images
- How to use graphs in documentation

**Run it:**
```bash
uv run python 05_visualization.py
```

**Note:** PNG export requires system graphviz. See `GRAPHVIZ_GUIDE.md` for setup instructions.

### LangGraph Studio (Visual Development)

**Concepts**: Visual graph editor, interactive testing, run visualization

LangGraph Studio provides a visual interface for developing and debugging your graphs locally.

**Setup:**
1. Install CLI: `uv sync` (already in dependencies)
2. Create `langgraph.json` (already created in project root)
3. Start Studio: `langgraph dev`

**Features:**
- Visual graph editor
- Interactive testing
- Run visualization with state inspection
- Time travel debugging
- Automatic code reloading

**See:** `LANGGRAPH_STUDIO_SETUP.md` for complete guide

### 06_langsmith_observability.py
**Concepts**: Observability, Tracing, Monitoring, LangSmith integration

Demonstrates:
- How to set up LangSmith for observability
- Automatic tracing of graph execution
- LLM call monitoring and metrics
- Custom trace metadata and tags
- Streaming with tracing

**Run it:**
```bash
# Set up your LangSmith API key first
export LANGSMITH_API_KEY=your_key_here
# Or add it to .env file

uv run python 06_langsmith_observability.py
```

**Note:** Requires LangSmith API key. Get one at https://smith.langchain.com/

## Installation

1. Install `uv` (if not already installed):
```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or with Homebrew
brew install uv

# Or with pip
pip install uv
```

2. Install dependencies:
```bash
uv sync
```

This will create a virtual environment and install all dependencies from `pyproject.toml`.

3. (Optional) For LLM features, set up Ollama:
```bash
# Install Ollama (if not already installed)
# macOS/Linux: curl -fsSL https://ollama.com/install.sh | sh
# Or visit: https://ollama.com/

# Start Ollama server
ollama serve

# Pull the Llama 3.1 model
ollama pull llama3.1

# Verify it works
ollama run llama3.1 "Hello"
```

## Key LangGraph Patterns

### Pattern 1: Linear Flow
```python
graph.add_edge(START, "node_a")
graph.add_edge("node_a", "node_b")
graph.add_edge("node_b", END)
```

### Pattern 2: Conditional Routing
```python
def route(state):
    return "path_a" if condition else "path_b"

graph.add_conditional_edges(
    "node",
    route,
    {"path_a": "node_a", "path_b": "node_b"}
)
```

### Pattern 3: Loop Until Condition
```python
def should_continue(state):
    return "continue" if not done else END

graph.add_conditional_edges(
    "process",
    should_continue,
    {"continue": "process", END: END}
)
```

### Pattern 4: Tool Usage
```python
graph.add_node("agent", agent_node)
graph.add_node("tools", ToolNode(tools))
graph.add_conditional_edges("agent", should_use_tools)
graph.add_edge("tools", "agent")
```

## State Management

LangGraph uses **reducer functions** to merge state updates:

```python
from typing_extensions import Annotated
import operator

class State(TypedDict):
    # Messages are appended
    messages: Annotated[list, operator.add]
    
    # Values are replaced
    counter: int
```

## Advanced Features

### Memory/Checkpointing
```python
from langgraph.checkpoint.memory import MemorySaver

memory = MemorySaver()
graph = graph.compile(checkpointer=memory)
```

### Streaming
```python
for chunk in graph.stream(initial_state):
    print(chunk)
```

### Human-in-the-Loop
```python
# Interrupt execution and wait for human input
config = {"configurable": {"thread_id": "1"}}
result = graph.invoke(state, config)
```

## Next Steps

1. **Explore the examples**: Run each tutorial file and understand the patterns
2. **Modify the examples**: Change the state, nodes, or edges to see how it affects behavior
3. **Build your own**: Create a graph for your specific use case
4. **Read the docs**: Visit [langchain-ai.github.io/langgraph](https://langchain-ai.github.io/langgraph)

## Common Use Cases

- **Chatbots**: Multi-turn conversations with memory
- **Agents**: Tool-using agents with reasoning
- **RAG Systems**: Retrieval-augmented generation workflows
- **Multi-Agent Systems**: Multiple agents working together
- **Workflow Automation**: Complex business logic with LLMs

## Resources

- [Official LangGraph Documentation](https://langchain-ai.github.io/langgraph)
- [LangGraph GitHub](https://github.com/langchain-ai/langgraph)
- [LangGraph Examples](https://github.com/langchain-ai/langgraph/tree/main/examples)

## Tips

1. **Start simple**: Begin with basic graphs before adding complexity
2. **Use type hints**: TypedDict helps catch errors early
3. **Test nodes individually**: Test each node function before building the graph
4. **Visualize**: Use `graph.get_graph().draw_mermaid_png()` to see your graph
5. **Handle errors**: Add error handling in nodes for production use

Happy building! 🚀
