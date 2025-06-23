LLM AI Agents - README.txt
==========================

Project Title:
--------------
LLM-Powered Multi-Agent Orchestration System

Project Overview:
-----------------
This project demonstrates how to orchestrate multiple LLM-powered agents to perform complex tasks collaboratively. It is built using LangGraph, LangChain, and Groq’s Gemma-2 9B or GPT-4o as the reasoning engine. The system includes a supervisor agent that coordinates the flow of tasks among other specialized agents (like search, math, or document analysis agents).

Folder Structure:
-----------------
- agent1.py, agent2.py, ... : Definitions for individual agents (e.g., researcher, math solver).
- supervisor.py             : Main orchestration logic using LangGraph.
- graph.py                  : StateGraph definition and flow logic.
- main.py                   : Entry point for the application or testing.
- ocr_module/, streamlit_ui/: (Optional) Document understanding components.

Setup Instructions:
-------------------
1. Clone the repository:
   git clone https://github.com/lharsha2005/llm-aiAgents.git

2. Install dependencies:
   pip install -r requirements.txt

3. Set environment variables:
   - OPENAI_API_KEY (for GPT-4o)
   - GROQ_API_KEY (for Groq models)
   - Any additional keys needed for LangChain tools.

4. Run the agent system:
   python main.py

5. (Optional) For Streamlit UI:
   streamlit run streamlit_ui/app.py

Features:
---------
- Multi-agent architecture using LangGraph.
- Supervisor-driven feedback loop and task delegation.
- Modular agents that can be replaced or upgraded easily.
- Optional OCR and document understanding modules integrated.

Use Cases:
----------
- Document Q&A (e.g., bank statements, payslips)
- Research assistance
- Math solving
- Data validation and correction via feedback loops

Technologies Used:
------------------
- Python
- LangGraph
- LangChain
- Groq (Gemma 2B/9B)
- OpenAI GPT-4o
- Streamlit (for UI)
- PaddleOCR / docTR (for OCR)

Credits:
--------
Created by Harsha Vardhan Leabaka

Notes:
------
- You can simulate agent collaboration, negotiation, and memory-based feedback loops.
- Ideal for prototyping intelligent document systems, research agents, and agent swarms.

