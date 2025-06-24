from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langgraph.types import Command
from State import State
from dotenv import load_dotenv
import os


load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# llm= ChatGroq(model="llama-3.3-70b-versatile",temperature=0.7)
llm=ChatOpenAI(model="gpt-4o",api_key=os.getenv("OPENAI_API_KEY"))

def run_agent1(state: State):
    history="\n".join(state["history"])
    extractor_data=state["extractor_data"]
    feedback=state["feedback"]
    prompt=f"""
    You are a optimistic legal advisor. 
    Here's the document content: 
    {extractor_data}
     
    Here's the conversation so far:
    {history}

    Here's the user feedback (if any):
    {feedback}

    Now, reply optimistically to the other agent's last message while keeping user feedback in mind.
    Keep it concise and bring in counterpoints.
    """

    res=llm.invoke(prompt).content

    return Command(
        update={"history": state["history"]+[f"optimistic Advisor: {res}"], "round": state["round"]+1},
        goto="debate"
    )