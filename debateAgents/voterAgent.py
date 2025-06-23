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

def voter_agent(state: State) -> State:
    full_debate = "\n".join(state["messages"])
    prompt = f"""
    Here's a full debate between two advisor agents on:
    "{state['question']}"

    Debate:
    {full_debate}

    Choose the stronger position: Agent 1 (Optimist) or Agent 2 (Skeptic).
    Justify your decision and clearly state the winner.
    Provide the Summarize the arugumet and provide the anser for the given question.
    """
    decision = llm.invoke(prompt).content
    return {**state, "answer": decision}
