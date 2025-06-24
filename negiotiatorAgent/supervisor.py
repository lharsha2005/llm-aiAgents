from State import State
from pydantic import BaseModel, Field
from typing import Literal
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langgraph.types import Command
from langgraph.graph import END
from dotenv import load_dotenv
import os

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# llm= ChatGroq(model="llama-3.3-70b-versatile",temperature=0.7)
llm=ChatOpenAI(model="gpt-4o",api_key=os.getenv("OPENAI_API_KEY"))

class Supervisor(BaseModel):
    name: Literal["ocr","extractor","debate","negotiatior","user","END"]=Field(
        description="Specifies the next worker in the pipeline: "
                    "'extractor' for pulling clauses like salary, dates, penalties, "
                    "'debate' for running a Debate from optismistic and skeptic point of view, "
                    "'negotiatior' Suggests edits,"
                    "'user' for gettign user feedback like agrees/disagrees or asks follow-up." 
                    "'END' for Ending when user ageers"
    )

    reson: str=Field(
        description="The reason for the decision, providing context on why a particular worker was chosen."
    )

def supervisor(state: State)->State:
    print("Entering Supervisor")
    ocr_text=state['ocr_data']
    extracted_data=state['extractor_data']
    debate_flag=state['debate_flag']
    negotiator_flag=state['negotiator_flag']
    history=state['history']
    feedback=state['feedback']

    prompt=f"""
    You are a supervisor for the following agents:
    1.'OcrAgent': OCR/docTR → extract clean text
    1.'ExtractorAgent': Pulls clauses like salary, dates, penalties
    2.'DebateAgent': Run a Debate from optismistic and skeptic point of view
    3.'NegotiatorAgent': Suggests edits
    4.'UserFeedbackNode': User agrees/disagrees or asks follow-up

    They collaboratively:
        -Analyze the document
        -Raise pros/cons    
        -Suggest changes
        -Let the user accept/reject/suggest alternatives

    ocr text is :{ocr_text}
    extracted data is:{extracted_data}
    debate over flag: {debate_flag}
    negotiatior over flag: {negotiator_flag}
    conversation so for is :{history}
    user feedback is: {feedback}

    **NOTE** ocr text is not extracted data. After ocr it needs to goto extractor

    Decision Logic:
    1.If ocr_text is not present goto 'ocr'
    2.Else If ocr_text is present and extracted data is not present goto 'extractor'
    3.Else If extracted data  is present and debate over flag is False goto 'debate'
    4.Else If debate over flag is True and negotiatior over flag is False goto 'negotiatior'
    5.Else If negotiatior over flag is True goto 'user'
    6.Else If feedback is present and feedback does not accept the answer from negotiatior goto 'debate'

    Your job is make the given agents work efficienty so that we can negotiate a legal documante.
    """

    res=llm.with_structured_output(Supervisor).invoke(prompt)
    goto=res.name
    print("="*140)
    print("Reason:",res.reson)
    print("="*140)
    print("supervisor->",goto)
    if goto=="END" or goto==END:
        goto=END
    return Command(goto=goto)