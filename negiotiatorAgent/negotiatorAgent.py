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

def negotiator(state: State):
    history="\n".join(state["history"])
    extractor_data=state["extractor_data"]
    feedback=state["feedback"]
    prompt=f"""
    You are a negotiation assistant specialized in reviewing formal documents (e.g., contracts, offer letters, invoices) and suggesting polite, professional edits to improve fairness or clarify ambiguous terms.

    You are given:
    1. Extracted key information from the document
    2. Arguments raised by the Optimist (supporting points)
    3. Concerns raised by the Skeptic (critical points)
    4. Optional user preferences or goals (e.g., "I want to reduce notice period")

    ---

    ## Your Goal:
    Generate a list of **professional and actionable suggestions** to renegotiate the terms in favor of the user, based on the Skeptic's concerns and any user preferences, without being too aggressive or confrontational.

    ---

    ### Input:
    - Extracted Info:
    {extractor_data}

    -Debate info:
    {history}

    - User Notes (if any):
    {feedback}

    ---

    ### Output Format (Paragraphs)(Example):
    give suggested changes in a paragraph format. easy to understan format.

    """

    res=llm.invoke(prompt).content
    print("negotiator->supervisor")
    return Command(
        update={"negotiator_data":res,"negotiator_flag":True},
        goto="supervisor"
    )