import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()
llm=ChatOpenAI(model="gpt-4o",api_key=os.getenv("OPENAI_API_KEY"))
# GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# llm= ChatGroq(model="llama-3.3-70b-versatile",temperature=0.7)

def run_qury(query: str,trnsations: dict):
    prompt=PromptTemplate.from_template(
        """
        you are an smart assistant how runs a quary on given transation history and givs answer.

        your give a transation history :
        {trnsations}

        and you a give a query to be run on the given transation history:
        {query}

        you are to use the given transations to give an appropriate answer to the query in the form of string.
        """
    )
    print("returning to supervisor")
    return llm.invoke(prompt.format(query=query,trnsations=trnsations))