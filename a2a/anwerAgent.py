import json
from graph import GraphRAG
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
load_dotenv
GROQ_API_KEY=os.getenv("GROQ_API_KEY")
llm=ChatGroq(model="llama-3.3-70b-versatile",temperature=0.6)

def process_question():
    with open("a2a_message.json") as f:
        msg = json.load(f)

    rag = GraphRAG()
    subgraph = rag.retrieve(msg["content"])

    if subgraph is None:
        answer = f"'{msg['content']}' not found in knowledge graph."
    else:
        graph_text = rag.to_text(subgraph)
        prompt=graph_text.join(msg["content"])
        answer = llm.invoke(prompt).content

    response = {
        "sender": msg["recipient"],
        "recipient": msg["sender"],
        "content": answer
    }

    with open("a2a_response.json", "w") as f:
        json.dump(response, f)
    print(f"Responded: {response}")

if __name__ == "__main__":
    process_question()
