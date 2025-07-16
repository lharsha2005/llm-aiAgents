from langchain_groq import ChatGroq
from langgraph.types import Command
from langgraph.graph import StateGraph,START,END

from State import State

def run_sentiment(state: State):
    """Analyze sentiment of the news content."""
    news = state["news"]
    history=state["history"]

    llm = ChatGroq(model="llama3-70b-8192", temperature=0.3)

    prompt = f"""
    You are a financial sentiment analysis agent.

    you are give a debate between on stocks:{history}

    Given the following stock news summary, return the overall sentiment 
    as one of these: "positive", "neutral", or "negative".

    News: {news}

    Sentiment:
    """

    sentiment = llm.invoke(prompt).content.strip().lower()

    # Just in case LLM gives extra text, we sanitize
    if "positive" in sentiment:
        sentiment = "positive"
    elif "negative" in sentiment:
        sentiment = "negative"
    else:
        sentiment = "neutral"

    return Command(update={"sentiment": sentiment},goto="data")
