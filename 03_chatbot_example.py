"""
LangGraph Tutorial - Part 3: Simple Chatbot
============================================

This tutorial demonstrates a basic chatbot using LangGraph.
Note: This requires an OpenAI API key or another LLM provider.
"""

from typing_extensions import TypedDict, Annotated
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
import operator
import os


# State for chatbot - uses messages list
class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], operator.add]


def chatbot_node(state: ChatState) -> dict:
    """
    Simple chatbot node that echoes back the user's message.
    In a real implementation, this would call an LLM.
    """
    messages = state["messages"]
    last_message = messages[-1]
    
    if isinstance(last_message, HumanMessage):
        # Simple echo response (replace with LLM call in production)
        response = f"Echo: {last_message.content}"
        print(f"Chatbot processing: {last_message.content}")
        return {
            "messages": [AIMessage(content=response)]
        }
    return {}


def build_chatbot_graph():
    """Build a simple chatbot graph"""
    graph_builder = StateGraph(ChatState)
    
    # Add the chatbot node
    graph_builder.add_node("chatbot", chatbot_node)
    
    # Define flow: START -> chatbot -> END
    graph_builder.add_edge(START, "chatbot")
    graph_builder.add_edge("chatbot", END)
    
    return graph_builder.compile()


# Advanced version with actual LLM (requires API key)
def build_llm_chatbot_graph():
    """
    Build a chatbot graph with actual LLM.
    Requires OPENAI_API_KEY environment variable.
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
            """Chatbot node that uses an actual LLM"""
            messages = state["messages"]
            print(f"LLM processing {len(messages)} messages")
            
            # Call the LLM with all messages
            response = llm.invoke(messages)
            return {"messages": [response]}
        
        graph_builder = StateGraph(ChatState)
        graph_builder.add_node("chatbot", llm_chatbot_node)
        graph_builder.add_edge(START, "chatbot")
        graph_builder.add_edge("chatbot", END)
        
        return graph_builder.compile()
    except Exception as e:
        print(f"Could not initialize LLM: {e}")
        print("Falling back to echo chatbot")
        return build_chatbot_graph()


if __name__ == "__main__":
    # Check if we have an API key
    has_api_key = os.getenv("OPENAI_API_KEY") or os.getenv("ANTHROPIC_API_KEY")
    
    if has_api_key:
        print("=" * 50)
        print("Building LLM-powered Chatbot")
        print("=" * 50)
        graph = build_llm_chatbot_graph()
    else:
        print("=" * 50)
        print("Building Echo Chatbot (no API key found)")
        print("Set OPENAI_API_KEY or ANTHROPIC_API_KEY for LLM chatbot")
        print("=" * 50)
        graph = build_chatbot_graph()
    
    # Simulate a conversation
    print("\nStarting conversation...\n")
    
    # First message
    state = {
        "messages": [HumanMessage(content="Hello! What is LangGraph?")]
    }
    result = graph.invoke(state)
    print(f"User: {state['messages'][0].content}")
    print(f"Assistant: {result['messages'][-1].content}\n")
    
    # Second message (continuing the conversation)
    state = {
        "messages": result["messages"] + [HumanMessage(content="Can you give me an example?")]
    }
    result = graph.invoke(state)
    print(f"User: {state['messages'][-1].content}")
    print(f"Assistant: {result['messages'][-1].content}\n")
