from typing import TypedDict
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

class State(TypedDict):
    messages: list[str]
    question: str
    answer: str
    round: int
    max_rounds: int

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

llm= ChatGroq(model="llama-3.3-70b-versatile",temperature=0.7)

def run_agent2(state: State):
    prev="\n".join(state["messages"])
    question=state["question"]
    prompt=f"""
    You are a skeptical advisor. 
    Answer the question: 
    {question}
     
    Here's the conversation so far:
    {prev}

    Now, reply critically to the other agent's last message.
    Keep it concise and bring in counterpoints.
    """

    res=llm.invoke(prompt).content

    return{**state, "messages": state["messages"]+[f"Agent 2: {res}"], "round": state["round"]+1}