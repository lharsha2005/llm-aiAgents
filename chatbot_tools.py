from typing import TypedDict
from typing_extensions import Annotated
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

from langchain_groq import ChatGroq
from langchain_tavily import TavilySearch
from langchain.schema import HumanMessage
import os
from dotenv import load_dotenv

import streamlit

load_dotenv()
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

tool = TavilySearch(max_results=2)
llm = ChatGroq(model="Gemma2-9b-It", temperature=0.6)
agent = llm.bind_tools([tool])

class State(TypedDict):
    messages: Annotated[list, add_messages]

graph = StateGraph(State)

tools_node = ToolNode(tools=[tool])

def chatBot(state: State):
    resp = agent.invoke(state["messages"])
    return {"messages": state["messages"] + [resp]}

graph.add_node("chatBot", chatBot)
graph.add_node("tools", tools_node)


graph.add_edge(START, "chatBot")
graph.add_conditional_edges("chatBot", tools_condition)
graph.add_edge("tools", "chatBot")
graph.add_edge("chatBot", END)

g = graph.compile()

def stream_graph_updates(user_input: str):
    data=None
    init_state = {"messages": [HumanMessage(content=user_input)]}
    for event in g.stream(init_state):
        for value in event.values():
            data=("Assistant:", value["messages"][-1].content)
            # return ("Assistant:", value["messages"][-1].content)
    return data

streamlit.title("Basic Chat Bot")
question=streamlit.text_input(label="Enter")

if question:
    streamlit.text_area(label="Entery", value="\n".join(stream_graph_updates(question)), height=300)
