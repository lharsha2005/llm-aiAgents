import os
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langgraph.types import Command
from langgraph.graph import END
from pydantic import BaseModel, Field
from typing import Literal
from dotenv import load_dotenv

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# llm= ChatGroq(model="llama-3.3-70b-versatile",temperature=0.7)
llm=ChatOpenAI(model="gpt-4o",api_key=os.getenv("OPENAI_API_KEY"))

class Checker(BaseModel):
    next: Literal["supervisor", "END"]=Field(
        description="Specifies the next worker in the pipeline: "
                    "'supervisor' if given conditions match, "
                    "'END' if given conditions do not match, "
    )

def run_checker(text: str):
    prompt=PromptTemplate.from_template(
        """
        text:{text}
        geivn text form ocr decide weather the given conditions satisfy.
        if the conditions satisfy goto supervisor next else end.
        conditions:
            1.if text is relavent to bank statements
            2.if final balance is less than 10000000
        """
    )

    res=llm.with_structured_output(Checker).invoke(prompt.format(text=text))

    goto=res.next

    if goto==END or goto=="END":
        goto==END

    print("cheker->",goto)
    return Command(
        update={"check": True},
        goto=goto
    )