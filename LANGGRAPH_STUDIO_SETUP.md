# LangGraph Studio Local Setup Guide

LangGraph Studio is a visual interface for developing, debugging, and monitoring your LangGraph applications locally.

## What is LangGraph Studio?

LangGraph Studio provides:
- **Visual Graph Editor** - See your graph structure
- **Interactive Testing** - Run and test your graphs in real-time
- **Run Visualization** - See execution flow and state changes
- **Debugging Tools** - Inspect intermediate states
- **Time Travel** - Step through execution history

## Quick Setup

### 1. Install LangGraph CLI and API

```bash
# Using uv (recommended)
uv sync

# This installs:
# - langgraph-cli[inmem] - CLI for running Studio
# - langgraph-api - API server for Studio

# Or using pip
pip install -U "langgraph-cli[inmem]" "langgraph-api"
```

**Note:** Both `langgraph-cli[inmem]` and `langgraph-api` are required. They're already in `pyproject.toml`.

### 2. Create Configuration File

Create a `langgraph.json` file in your project root:

```json
{
  "dependencies": ["."],
  "graphs": {
    "chatbot": {
      "path": "03_chatbot_example:build_chatbot_graph",
      "description": "Simple chatbot example"
    },
    "tools_agent": {
      "path": "04_tools_example:build_agent_graph",
      "description": "Agent with tools"
    },
    "observable_chatbot": {
      "path": "06_langsmith_observability:build_chatbot_graph",
      "description": "Chatbot with LangSmith observability"
    }
  },
  "env": ".env"
}
```

**Important:** The `dependencies` field is required. Use `["."]` to include the current directory.

### 3. Start LangGraph Studio

```bash
langgraph dev
```

This will:
- Start a local server at `http://127.0.0.1:2024`
- Automatically open LangGraph Studio in your browser
- Watch for code changes and reload automatically

### 4. Access Studio

If it doesn't open automatically, navigate to:

```
https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024
```

Or use the local URL:
```
http://127.0.0.1:2024
```

## Configuration Details

### langgraph.json Structure

```json
{
  "graphs": {
    "graph_name": {
      "path": "module:function",
      "description": "Optional description"
    }
  },
  "env": ".env"
}
```

**Path Format:**
- `module` - Python file name (without .py)
- `function` - Function that returns a compiled graph

**Example:**
```json
{
  "graphs": {
    "my_chatbot": {
      "path": "03_chatbot_example:build_llm_chatbot_graph",
      "description": "LLM-powered chatbot"
    }
  }
}
```

### Multiple Graphs

You can register multiple graphs:

```json
{
  "graphs": {
    "basic": {
      "path": "01_basic_graph:build_graph"
    },
    "conditional": {
      "path": "02_conditional_edges:build_graph"
    },
    "chatbot": {
      "path": "03_chatbot_example:build_chatbot_graph"
    },
    "tools": {
      "path": "04_tools_example:build_agent_graph"
    }
  },
  "env": ".env"
}
```

## Using Studio Features

### 1. Visual Graph Editor

- See your graph structure as a visual diagram
- Nodes and edges are displayed
- Conditional routing is highlighted

### 2. Interactive Testing

- Enter input in the UI
- Run your graph interactively
- See real-time execution

### 3. Run Visualization

- View execution timeline
- See which nodes executed
- Inspect state at each step

### 4. State Inspection

- Click on any node to see:
  - Input state
  - Output state
  - Execution time
  - Any errors

### 5. Time Travel Debugging

- Step backward through execution
- See how state changed over time
- Identify where issues occurred

## Example: Setting Up Your Tutorial Graphs

Create `langgraph.json`:

```json
{
  "graphs": {
    "basic_graph": {
      "path": "01_basic_graph:build_graph",
      "description": "Basic graph with nodes and edges"
    },
    "conditional_graph": {
      "path": "02_conditional_edges:build_graph",
      "description": "Graph with conditional routing"
    },
    "chatbot": {
      "path": "03_chatbot_example:build_chatbot_graph",
      "description": "Simple echo chatbot"
    },
    "llm_chatbot": {
      "path": "03_chatbot_example:build_llm_chatbot_graph",
      "description": "LLM-powered chatbot (requires API key)"
    },
    "tools_agent": {
      "path": "04_tools_example:build_agent_graph",
      "description": "Agent with calculator and weather tools"
    },
    "observable_chatbot": {
      "path": "06_langsmith_observability:build_chatbot_graph",
      "description": "Chatbot with LangSmith tracing"
    }
  },
  "env": ".env"
}
```

## Advanced Features

### Debugging Mode

Start with debugging enabled:

```bash
# Install debugpy first
uv add debugpy

# Start with debug port
langgraph dev --debug-port 5678
```

Then attach your IDE debugger to port 5678.

### VS Code Debug Configuration

Add to `.vscode/launch.json`:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Attach to LangGraph",
      "type": "debugpy",
      "request": "attach",
      "connect": {
        "host": "localhost",
        "port": 5678
      }
    }
  ]
}
```

### Custom Port

```bash
langgraph dev --port 3000
```

### Watch Mode

Studio automatically watches for code changes and reloads. No need to restart!

## Troubleshooting

### "Graph not found"

- Check that your `langgraph.json` path is correct
- Ensure the function returns a compiled graph
- Verify the module can be imported

### "Required package 'langgraph-api' is not installed"

If you see this error:

```bash
# Make sure both packages are installed
uv sync

# Or explicitly install
uv add "langgraph-cli[inmem]" "langgraph-api"

# Verify installation
uv run python -c "import langgraph_api; print('OK')"
```

The `langgraph-api` package should be automatically installed with `langgraph-cli[inmem]`, but if not, add it explicitly to your dependencies.

### "Port already in use"

```bash
# Use a different port
langgraph dev --port 3000
```

### "Studio won't connect"

- Check that the server is running
- Verify the URL: `http://127.0.0.1:2024`
- Try the cloud studio URL with baseUrl parameter

### "Graph execution fails"

- Check your `.env` file for required API keys
- Verify all dependencies are installed
- Check the terminal for error messages

## Integration with LangSmith

LangGraph Studio works seamlessly with LangSmith:

1. **Enable Tracing** - Set `LANGSMITH_API_KEY` in `.env`
2. **View Traces** - Runs in Studio are automatically traced
3. **Compare Runs** - Use LangSmith dashboard to compare different runs
4. **Debug Issues** - Use Studio for local debugging, LangSmith for production monitoring

## Best Practices

1. **Organize Graphs** - Use descriptive names in `langgraph.json`
2. **Add Descriptions** - Help others understand your graphs
3. **Use .env** - Keep API keys out of code
4. **Test Locally** - Use Studio for development, LangSmith for production
5. **Version Control** - Commit `langgraph.json` but not `.env`

## Example Workflow

```bash
# 1. Set up your graph
# (create your graph file)

# 2. Add to langgraph.json
# (register your graph)

# 3. Start Studio
langgraph dev

# 4. Test in Studio UI
# (interact with your graph visually)

# 5. View traces in LangSmith
# (if LANGSMITH_API_KEY is set)
```

## Next Steps

1. Create `langgraph.json` for your project
2. Run `langgraph dev`
3. Explore your graphs in Studio
4. Test different inputs
5. Debug issues visually
6. View traces in LangSmith dashboard

Happy developing! 🚀

