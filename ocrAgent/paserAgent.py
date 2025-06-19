import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_community.chat_models import ChatOllama
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# llm= ChatGroq(model="llama-3.3-70b-versatile",temperature=0.7)
llm=ChatOpenAI(model="gpt-4o",api_key=os.getenv("OPENAI_API_KEY"))

def run_paser(text: str):
    prompt=PromptTemplate.from_template(
        """
        Given the bank statement text:
        {text}

        Try to fill in any missing fields accurately.

        Do not add any extra fields.Only include: date, details, CHQ/REF NO, Debit/Credit, Amount, Balance.

        Respond with a JSON dictionary.
        """
    )
    print("returning to supervisor")
    return llm.invoke(prompt.format(text=text))