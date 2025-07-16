from langchain_groq import ChatGroq
from langchain_tavily import TavilySearch
from langgraph.types import Command
from State import State
import os
from dotenv import load_dotenv

from langgraph.graph import START,END,StateGraph

load_dotenv()
TAVILY_API_KEY=os.getenv("TAVILY_API_KEY")
GROQ_API_KEY=os.getenv("GROQ_API_KEY")

def run_news(state: State):
    """Used to get real time news about intrested stocks"""
    tool=TavilySearch(max_results=5,topic="news")
    llm=ChatGroq(model="llama-3.3-70b-versatile",temperature=0.6)
    llm.bind_tools([tool])

    stock=state["stock"]
    news_results = tool.invoke({"query": f"{stock} stock news"})
    prompt=f"""
    The following are real-time news snippets about the stock '{stock}':
    
    {news_results}

    Summarize the key points that might affect the stock price.
    """

    result=llm.invoke(prompt).content

    return Command(update={"news":result},goto="debate")
