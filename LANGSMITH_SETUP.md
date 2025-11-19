# LangSmith Setup Guide

LangSmith provides observability, tracing, and monitoring for your LangGraph applications.

## What is LangSmith?

LangSmith is a platform that helps you:
- **Trace** your LangGraph execution in real-time
- **Monitor** LLM calls, token usage, and costs
- **Debug** issues with detailed execution logs
- **Analyze** performance and optimize your graphs
- **Evaluate** your agents with datasets

## Quick Setup

### 1. Get Your API Key

1. Sign up at [https://smith.langchain.com/](https://smith.langchain.com/)
2. Go to Settings → API Keys
3. Create a new API key
4. Copy the key

### 2. Add to Environment

**Option A: Environment Variable**
```bash
export LANGSMITH_API_KEY=your_api_key_here
```

**Option B: .env File (Recommended)**
```bash
# .env
LANGSMITH_API_KEY=your_api_key_here
LANGCHAIN_PROJECT=langraph-tutorial  # Optional: project name
```

### 3. Install Dependencies

The `langsmith` package is already in `pyproject.toml`. Just run:

```bash
uv sync
```

### 4. Run the Example

```bash
uv run python 06_langsmith_observability.py
```

## Configuration Options

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `LANGSMITH_API_KEY` | Yes | - | Your LangSmith API key |
| `LANGCHAIN_API_KEY` | Yes* | - | Alternative name for API key |
| `LANGCHAIN_TRACING_V2` | No | `false` | Enable tracing (set to `true`) |
| `LANGCHAIN_PROJECT` | No | `default` | Project name in LangSmith |
| `LANGCHAIN_ENDPOINT` | No | `https://api.smith.langchain.com` | API endpoint |

*Either `LANGSMITH_API_KEY` or `LANGCHAIN_API_KEY` works

### Basic Setup in Code

```python
import os
from langsmith import Client
from langchain_core.tracers.context import tracing_v2_enabled

# Enable tracing
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "my-project"

# Create client
client = Client()

# Use with tracing
with tracing_v2_enabled(client=client):
    result = graph.invoke(input_state)
```

## What Gets Traced?

LangSmith automatically traces:

1. **Graph Execution**
   - Each node execution
   - State transitions
   - Edge routing decisions

2. **LLM Calls**
   - Input prompts
   - Output responses
   - Token usage
   - Latency
   - Costs

3. **Tool Calls**
   - Tool invocations
   - Inputs and outputs
   - Execution time

4. **Errors**
   - Exception details
   - Stack traces
   - Context at failure point

## Viewing Traces

1. Go to [https://smith.langchain.com/](https://smith.langchain.com/)
2. Navigate to your project
3. Click on any trace to see:
   - Execution timeline
   - Node inputs/outputs
   - LLM call details
   - Performance metrics

## Advanced Features

### Custom Metadata

```python
config = {
    "run_name": "my-custom-run",
    "tags": ["production", "v2"],
    "metadata": {
        "user_id": "user_123",
        "version": "1.0.0"
    }
}

graph.invoke(state, config)
```

### Filtering Traces

In LangSmith UI:
- Filter by tags
- Search by run name
- Filter by date range
- Filter by errors

### Exporting Traces

```python
from langsmith import Client

client = Client()
runs = client.list_runs(project_name="my-project")
# Export or analyze runs
```

## Troubleshooting

### "API key not found"
- Make sure `LANGSMITH_API_KEY` is set in your environment
- Check your `.env` file is loaded
- Verify the key is correct in LangSmith dashboard

### "No traces appearing"
- Ensure `LANGCHAIN_TRACING_V2=true` is set
- Check your API key is valid
- Verify network connectivity to LangSmith

### "Project not found"
- Projects are created automatically
- Check the project name in `LANGCHAIN_PROJECT`
- Verify you have access in LangSmith dashboard

## Best Practices

1. **Use Project Names**
   ```python
   os.environ["LANGCHAIN_PROJECT"] = "production-chatbot"
   ```

2. **Add Tags for Organization**
   ```python
   config = {"tags": ["production", "chatbot", "v2"]}
   ```

3. **Set Run Names**
   ```python
   config = {"run_name": "user-session-123"}
   ```

4. **Monitor Costs**
   - Check token usage in LangSmith
   - Set up alerts for high costs
   - Track costs per project

5. **Use for Debugging**
   - Inspect failed runs
   - Compare successful vs failed traces
   - Analyze performance bottlenecks

## Example Workflow

```python
from langsmith import Client
from langchain_core.tracers.context import tracing_v2_enabled

# Setup
client = Client()
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "my-chatbot"

# Run with tracing
with tracing_v2_enabled(client=client):
    result = graph.invoke(
        {"messages": [HumanMessage(content="Hello!")]},
        config={"run_name": "test-run", "tags": ["demo"]}
    )

# View in LangSmith dashboard
print("View trace at: https://smith.langchain.com/")
```

## Resources

- [LangSmith Documentation](https://docs.smith.langchain.com/)
- [LangSmith Dashboard](https://smith.langchain.com/)
- [LangGraph Tracing Guide](https://langchain-ai.github.io/langgraph/how-tos/observability/)

## Next Steps

1. Run `06_langsmith_observability.py` to see examples
2. Check your LangSmith dashboard for traces
3. Experiment with custom metadata and tags
4. Set up alerts for errors or high latency
5. Use datasets to evaluate your graphs

Happy tracing! 🔍

