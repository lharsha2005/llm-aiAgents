from langchain_groq import ChatGroq
from langgraph.types import Command
from langgraph.graph import START,END,StateGraph

from debate_agent import debate
from agent1 import run_agent1
from agent2 import run_agent2
from news_agent import run_news
from sentiment_agent import run_sentiment
from data_agent import run_stock_data
from State import State

def run_predictor_llm(state: State):
    llm = ChatGroq(model="llama3-70b-8192", temperature=0.4)

    prompt = f"""
    Based on the following information, provide a final trading recommendation
    (one of: "Buy", "Sell", "Hold").

    Stock: {state['stock']}
    Sentiment: {state['sentiment']}
    Stock Price Change: {state['stock_data']}
    News Summary: {state['news']}

    Recommendation:
    """

    rec = llm.invoke(prompt).content
    return Command(update={"recommendation": rec})

workflow=StateGraph(State)
workflow.add_node("news",run_news)
workflow.add_node("debate",debate)
workflow.add_node("agent_1",run_agent1)
workflow.add_node("agent_2",run_agent2)
workflow.add_node("sentiment",run_sentiment)
workflow.add_node("data",run_stock_data)
workflow.add_node("predictor",run_predictor_llm)
workflow.add_edge(START,"news")
workflow.add_edge("predictor",END)
graph=workflow.compile()

input={"stock":"INTC","max_rounds":2,"round":1,"history":[]}
out=graph.invoke(input)
print(out["recommendation"])
