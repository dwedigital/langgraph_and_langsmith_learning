# Quick Start Guide

## Installation

### 1. Install uv (if not already installed)

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or with Homebrew
brew install uv

# Or with pip
pip install uv
```

### 2. Install project dependencies

```bash
# This creates a virtual environment and installs all dependencies
uv sync
```

### 3. Activate the virtual environment (if needed)

```bash
# uv automatically manages the virtual environment
# You can run scripts directly with:
uv run python 01_basic_graph.py

# Or activate manually:
source .venv/bin/activate  # macOS/Linux
# or
.venv\Scripts\activate  # Windows
```

## Run the Tutorials

Start with the simplest example and work your way up:

### 1. Basic Graph (No dependencies on external APIs)
```bash
uv run python 01_basic_graph.py
```

This demonstrates:
- State definition
- Node creation
- Edge connections
- Graph execution

### 2. Conditional Edges
```bash
uv run python 02_conditional_edges.py
```

This shows:
- Dynamic routing based on state
- Conditional logic in graphs

### 3. Simple Chatbot
```bash
# Without Ollama (echo bot)
uv run python 03_chatbot_example.py

# With Ollama running (uses Llama 3.1)
# Make sure Ollama is running: ollama serve
# And model is installed: ollama pull llama3.1
uv run python 03_chatbot_example.py
```

### 4. Tools Example
```bash
uv run python 04_tools_example.py
```

This demonstrates:
- Tool definition
- Tool execution
- Conditional tool routing

### 5. Visualization
```bash
uv run python 05_visualization.py
```

This demonstrates:
- Graph visualization methods
- Mermaid diagrams
- PNG export

### 6. LangSmith Observability
```bash
# Set up LangSmith API key first
export LANGSMITH_API_KEY=your_key_here
uv run python 06_langsmith_observability.py
```

This demonstrates:
- Observability and tracing
- LLM call monitoring
- Performance metrics
- Debugging with LangSmith

## LangGraph Studio (Visual Development)

LangGraph Studio provides a visual interface for developing and debugging your graphs.

### Quick Start

```bash
# 1. Install dependencies (already in pyproject.toml)
uv sync

# 2. Start Studio
langgraph dev
```

This will:
- Start a local server at `http://127.0.0.1:2024`
- Open LangGraph Studio in your browser
- Show all your registered graphs

### Access Studio

If it doesn't open automatically:
```
https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024
```

### Features

- **Visual Graph Editor** - See your graph structure
- **Interactive Testing** - Run graphs in real-time
- **Run Visualization** - See execution flow
- **State Inspection** - Debug at each step
- **Time Travel** - Step through execution history

See `LANGGRAPH_STUDIO_SETUP.md` for complete guide.

## Understanding the Code

Each tutorial file follows this pattern:

1. **Import dependencies**
2. **Define State** - What data flows through the graph
3. **Define Nodes** - Functions that process state
4. **Build Graph** - Connect nodes with edges
5. **Run Graph** - Execute with initial state

## Key Concepts to Learn

### State
```python
class State(TypedDict):
    messages: Annotated[list[str], operator.add]  # Accumulated
    counter: int  # Replaced
```

### Nodes
```python
def my_node(state: State) -> dict:
    # Process state
    return {"counter": state["counter"] + 1}  # Return updates
```

### Edges
```python
graph.add_edge(START, "node_a")  # Regular edge
graph.add_conditional_edges("node", route_func)  # Conditional
```

## Next Steps

1. Run each example
2. Modify the code to see how changes affect behavior
3. Combine patterns from different examples
4. Build your own graph for your use case

## Troubleshooting

**Import errors?**
- Make sure you've run `uv sync` to install dependencies
- Or use `uv run python script.py` to run scripts in the uv environment

**LLM errors?**
- Examples 1, 2, and 4 don't need LLMs
- Example 3 works without Ollama (echo mode) or with Ollama running locally
- Make sure Ollama is running: `ollama serve`
- Make sure llama3.1 is installed: `ollama pull llama3.1`

**Graph visualization not working?**
- Requires graphviz: `brew install graphviz` (Mac) or `apt-get install graphviz` (Linux)
- This is optional - the examples work without it
