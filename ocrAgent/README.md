
Intelligent Bank Statement Q&A System
=====================================

This project is an intelligent document processing system that allows users to upload images of bank statements
and ask questions like "What were the transactions on 30/05/2020?". It uses a combination of OCR, 
Large Language Models (LLMs), and a supervisor-based agentic flow to extract, validate, parse, 
and answer questions based on the contents of the bank statement.

Core Components:
----------------

1. Streamlit UI (main.py)
   - Lets user upload an image and type a question.
   - Displays the final answer and debug information.

2. LangGraph Workflow (graph.py)
   - Models the pipeline with named agents as nodes:
     OCR → Checker → Parser → Query
   - Uses a Supervisor to dynamically decide the next step.

3. Agents:
   - ocrAgent.py:
     Uses PaddleOCR to extract text from the image.
   - checkerAgent.py:
     Validates whether the text meets specific conditions before further processing.
   - paserAgent.py:
     Parses unstructured OCR text into a structured JSON dictionary of transactions.
   - queryAgent.py:
     Answers user-defined questions using parsed JSON data.
   - supervisor.py:
     Directs the workflow by deciding which agent should run next based on the current state.

Important Notes:
----------------

- Uses OpenAI's GPT-4o as the primary LLM.
- Supports condition-checking: If the statement or question doesn't meet the criteria, it ends early.
- All transitions between steps are governed by a LangGraph state machine.

To Run:
-------
1. Install dependencies: pip install -r requirements.txt
2. Set your API key in `.env`:
    OPENAI_API_KEY=your_key_here
3. Run the app: streamlit run main.py

Example:
--------
Upload a bank statement image and ask:
  "What are the total debits in June 2023?"
Or:
  "List transactions above ₹10,000"

This system is modular and can be extended with memory, feedback loops, or even vector DBs for persistent storage.
