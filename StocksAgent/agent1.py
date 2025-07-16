from langchain_groq import ChatGroq
# from langchain_openai import ChatOpenAI
from langgraph.types import Command
from State import State
from dotenv import load_dotenv
import os


load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

llm= ChatGroq(model="llama-3.3-70b-versatile",temperature=0.7)
# llm=ChatOpenAI(model="gpt-4o",api_key=os.getenv("OPENAI_API_KEY"))

def run_agent1(state: State):
    history="\n".join(state["history"])
    news=state["news"]

    prompt=f"""
    You are a stocks advisor. 
    Here's the realtime new on the intrsted stock: 
    {news}
     
    Here's the conversation so far:
    {history}

    Now, reply optimistically to the other agent's last message.
    Keep it concise and bring in counterpoints.
    """

    res=llm.invoke(prompt).content

    return Command(
        update={"history": state["history"]+[f"optimistic Advisor: {res}"], "round": state["round"]+1},
        goto="debate"
    )