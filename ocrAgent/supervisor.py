import os
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langgraph.types import Command
from pydantic import BaseModel, Field
from typing import TypedDict, Literal
from typing_extensions import Annotated
from dotenv import load_dotenv

class State(TypedDict):
    img_path: str
    ocr_text: str
    check: bool
    corrected_data: dict
    question: str
    answer: str
  

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# llm= ChatGroq(model="llama-3.3-70b-versatile",temperature=0.7)
llm=ChatOpenAI(model="gpt-4o",api_key=os.getenv("OPENAI_API_KEY"))

class Supervisor(BaseModel):
    name: Literal["ocr","paser","checker","query"]=Field(
        description="Specifies the next worker in the pipeline: "
                    "'ocr' for extracting text form image, "
                    "'checker' for checking if ocr text is relavent, "
                    "'paser' for converting ocr text to ordered json format.,"
                    "'query' for answering user query on extraced json data." 
    )

    reson: str=Field(
        description="The reason for the decision, providing context on why a particular worker was chosen."
    )

def supervisor(state: State):
    """
    Supervisor node for routing tasks based on the current state and LLM response.
    Args:
        state (MessagesState): The current state containing message history.
    Returns:
        Command: A command indicating the next state or action.
    """
    print("enter supervisor")
    prompt=PromptTemplate.from_template(
        """
       You are a workflow supervisor managing a team of four agents: ocr, paser, checker and query. Your role is to direct the flow of tasks by selecting the next agent based on the current stage of the workflow. For each task, provide a clear rationale for your choice, ensuring that the workflow progresses logically, efficiently, and toward a timely completion.

        **Team Members**:
        1.ocr: extracts text form a given image.
        2.checker: checks if the ocr text meets certain conditions; if not, it ends.
        3.paser: converts the ocr text to structured json data.
        4.query: answers user query using json data from paser.

        The current state is:
        - OCR Text is present: {has_ocr_text}
        - Checked flag is: {checked}
        - Corrected data is present: {has_corrected_data}
        - User question is: "{question}"
        - Current answer is: "{answer}"

        **Decision Logic**:
        1. If OCR text is not present, go to ocr
        2. Else if Checked flag is False, go to checker
        3. Else if corrected data is present and no answer yet, go to query
        4. Else end

        Based on the above, choose the correct next agent and explain your reasoning.
    """
    )

    res=llm.with_structured_output(Supervisor).invoke(
    prompt.format_prompt(
        has_ocr_text=bool(state.get("ocr_text")),
        checked=state.get("check"),
        has_corrected_data=bool(state.get("corrected_data")),
        question=state.get("question", ""),
        answer=state.get("answer", ""),
    )
)
    print("#"*80)
    print("reson:",res.reson)
    print("#"*80)
    print()
    print("supervisor->",res.name)
    return Command(
        goto=res.name   
    )
