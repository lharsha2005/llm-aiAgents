from langchain_groq import ChatGroq
from langgraph.graph import END
from langgraph.types import Command
from State import State
from dotenv import load_dotenv
import os

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

llm= ChatGroq(model="llama-3.3-70b-versatile",temperature=0.7)
# llm=ChatOpenAI(model="gpt-4o",api_key=os.getenv("OPENAI_API_KEY"))

def run_query(state: State)->State:
    user_input = state["question"]
    ocr_text=state["ocr_text"]
    img_path=state["img_path"]
    prompt=f"""
    your are an expert in Banking domian.
    
    Here's the document provided(If any): {ocr_text}
    Here's the question : {user_input}

    Answer the question if and only if both question and documetn provided are related to banking domain.
    Else answer 'conditions not satisfied'.
    """

    if user_input==None:
        print("query->END")
        return Command(update={"answer":"no question provided."},goto=END)

    answer = llm.invoke(prompt).content

    if img_path:
            os.remove(img_path)  
    print("query->END")
    return Command(update={"answer":answer},goto=END)
