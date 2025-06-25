from State import State
from pydantic import BaseModel, Field
from typing import Literal
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langgraph.types import Command
from dotenv import load_dotenv
import os

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

llm= ChatGroq(model="llama-3.3-70b-versatile",temperature=0.7)
# llm=ChatOpenAI(model="gpt-4o",api_key=os.getenv("OPENAI_API_KEY"))

class Supervisor(BaseModel):
    name: Literal["ocr","query"]=Field(
        description="Specifies the next worker in the pipeline: "
                    "'ocr for extracting image text"
                    "'query' for answering the user question." 
    )

    reson: str=Field(
        description="The reason for the decision, providing context on why a particular worker was chosen."
    )


def supervisor(state: State)->State:
    img_path=state["img_path"]
    question=state["question"]
    ocr_text=state["ocr_text"]
    answer=state["answer"]

    prompt=f"""
    You are a supervisor for a banking chatbot the following agents:
    1.'OcrAgent': OCR/docTR → extract clean text.
    2.'query': answer user question.

    ocr text is: {ocr_text}
    image path is: {img_path}
    user question is: {question}
    answer to question is: {answer}

    Decision Logic:
    1.If image path is present and ocr text is not present goto 'ocr'.
    2.Else If ocr text is present and question is present goto 'query'.

    Your job is make the given agents work efficienty so that we can negotiate a legal documante.
    """

    res=llm.with_structured_output(Supervisor).invoke(prompt)
    goto=res.name

    print("="*140)
    print("Reason:",res.reson)
    print("="*140)
    print("supervisor->",goto)

    return Command(goto=goto)