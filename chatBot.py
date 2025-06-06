from typing import TypedDict
from typing_extensions import Annotated
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

from langchain_ollama import ChatOllama

import streamlit

class State(TypedDict):
    message: Annotated[list,add_messages]

graph=StateGraph(State)

llm=ChatOllama(model="tinyllama")

def chatBot(state:State):
    return {"message":[llm.invoke(state["message"])]}

graph.add_node("chatBot",chatBot)
graph.add_edge(START, "chatBot")

g=graph.compile()

def stream_graph_updates(user_input: str):
    data=[]
    for event in g.stream({"message": [{"role": "user", "content": user_input}]}):
        for value in event.values():
            return("Assistant:", value["message"][-1].content)

streamlit.title("Basic Chat Bot")
if "chat_history" not in streamlit.session_state:
    streamlit.session_state.chat_history = []
question=streamlit.text_input(label="Enter")

if question:
    # streamlit.session_state.chat_history.append(f"you:{question}")

    # streamlit.session_state.chat_history.append(f"AI:{stream_graph_updates(question)}")
    streamlit.text_area(label="Entery", value="\n".join(stream_graph_updates(question)), height=300)
    

# if streamlit.session_state.chat_history:
#     streamlit.text_area(label="Entery", value="\n".join(streamlit.session_state.chat_history), height=300)
# while True:
#     if(question=='q'):
#         break
#     stream_graph_updates(question,text)