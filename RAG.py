import os
from doctr.io import DocumentFile
from doctr.models import ocr_predictor
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
load_dotenv()

# Load Groq API key
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Step 1: OCR for Multi-page PDFs using doctr
def extract_text_from_pdf(pdf_path):
    model = ocr_predictor(pretrained=True)
    doc = DocumentFile.from_pdf(pdf_path)
    result = model(doc)
    
    # Combine all pages into one text string
    text = ""
    for page in result.pages:
        text += page.render() + "\n"
    return text.replace("\n", " ")

# Step 2: Chunking (simple word chunking)
def chunk_text(text, chunk_size=300):
    words = text.split()
    return [' '.join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]

# Step 3: Embedding and FAISS indexing
def build_vector_store(chunks):
    embedder = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = embedder.encode(chunks)
    dim = embeddings[0].shape[0]
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embeddings))
    return index, chunks, embedder

# Step 4: RAG querying
def query_with_rag(query, index, chunks, embedder):
    query_embedding = embedder.encode([query])
    D, I = index.search(np.array(query_embedding), k=3)
    context = "\n".join([chunks[i] for i in I[0]])

    prompt = PromptTemplate.from_template(
        "Use the context below to answer the question.\n\nContext:\n{context}\n\nQuestion: {question}\nAnswer:"
    )

    llm = ChatGroq(model="llama3-70b-8192", temperature=0.2)
    chain = prompt | llm
    answer = chain.invoke({"context": context, "question": query})
    return answer.content

# === Runner ===
if __name__ == "__main__":
    pdf_path = "Others(crldocs).pdf"  # ⬅️ Replace with your multi-page PDF

    print("Running OCR with docTR...")
    extracted_text = extract_text_from_pdf(pdf_path)
    print("Extracted Text Sample:\n", extracted_text[:300], "\n")

    print("Chunking and Embedding...")
    chunks = chunk_text(extracted_text)
    index, chunks, embedder = build_vector_store(chunks)

    print("Ask a question based on the scanned PDF.")
    while True:
        query = input("Your question: ")
        if query.lower() in ['exit', 'quit']:
            break
        answer = query_with_rag(query, index, chunks, embedder)
        print("Answer:", answer)
