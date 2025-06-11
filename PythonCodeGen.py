from typing import TypedDict
from typing_extensions import Annotated

from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode,tools_condition
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.graph import StateGraph,START,END
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_experimental.utilities import PythonREPL
from langchain_core.tools import Tool

import os
from dotenv import load_dotenv
import streamlit

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

class State(TypedDict):
    messages:Annotated[list,add_messages]

repl=Tool(name="pythonREPL",func=PythonREPL.run,description="Execute Python code. Input must be valid Python code.")
toolNode=ToolNode([repl])

llm=ChatGroq(model="Gemma2-9b-It", temperature=0.6)
prompt=ChatPromptTemplate.from_template("""
white Python code for:{request}
-Give only exectable code.
-Provide with all required imports
-Do not give explanations
-Do not give notes
-Direct executable code
""")

def execute_python(code: str):
    try:
        result = PythonREPL().run(code)
        return f"Execution successful\n{result}"
    except Exception as e:
        return f"Execution failed\n{str(e)}"

def generateCode(state: State):
    user=state["messages"][-1].content
    chain=prompt | llm
    res = chain.invoke({"request":user})
    return{
        "messages":[res]
    }

def runCode(state: State):
    msg=state["messages"][-1]
    if isinstance(msg,AIMessage):
        code=msg.content
        result=execute_python(code)
        return{
            "messages":[AIMessage(content=f"{result}")]
        }
    return state

graph=StateGraph(State)
graph.add_node("generate",generateCode)
graph.add_node("run",runCode)
graph.add_edge(START,"generate")
graph.add_edge("generate","run")
graph.add_edge("run",END)

g=graph.compile()

def run(input: str):
    result=g.invoke({"messages": [HumanMessage(content=input)]})
    for msg in result["messages"]:
        if isinstance(msg, AIMessage):
            return(f"\nAssistant:\n{msg.content}")

streamlit.title("Python Code Generator")
question=streamlit.text_input(label="Enter")

if question:
    streamlit.text_area(label="Entery", value="".join(run(question)), height=300)
