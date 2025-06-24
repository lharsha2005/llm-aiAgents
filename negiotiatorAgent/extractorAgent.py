from State import State
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

def extractor(state: State)->State:
    ocr_text=state['ocr_data']

    prompt=f"""
    You are an expert document information extractor.

    Given a document text from ocr agent(e.g., a contract, invoice, or offer letter), your task is to extract key structured information from the text. Extract only what is present explicitly or can be inferred with high confidence.

    Return your output as a JSON object in this format:

    ```json
    "document_type": "Employment Contract | Invoice | NDA | Other",
    "parties_involved": ["Party A", "Party B"],
    "effective_date": "...",
    "termination_clause": "...",
    "salary_or_payment_terms": "...",
    "bonus_or_incentives": "...",
    "working_hours": "...",
    "leave_policy": "...",
    "probation_period": "...",
    "confidentiality_clause": "...",
    "notice_period": "...",
    "jurisdiction": "...",
    "penalty_or_fine_clauses": "...",
    "missing_or_ambiguous_sections": [ "...", "..."]
    ```

    If a field is not present or unclear, return `null` or include a note under `missing_or_ambiguous_sections`.

    ocr text:{ocr_text}
    """

    result=llm.invoke(prompt).content
    print("extractor->supervisor")

    return Command(update={"extractor_data":result},goto="supervisor")