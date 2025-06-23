debateAgents - README.txt
=========================

Project Submodule:
------------------
LLM-Powered Debate Agent Framework

Purpose:
--------
This module demonstrates a multi-agent debate framework using LangGraph, where two or more agents present their arguments on a given topic. A supervisor agent orchestrates the debate, evaluates responses, and optionally declares a winner.

Key Concepts:
-------------
- Simulated agentic debates using LLMs
- Multi-turn argument generation
- Supervisor with memory and reasoning
- Feedback loop to improve agent responses

Folder Contents:
----------------
- agent1.py         : Agent 1 definition (e.g., "Pro" side)
- agent2.py         : Agent 2 definition (e.g., "Con" side)
- supervisor.py     : Coordinates the debate, evaluates arguments, tracks rounds
- graph.py          : LangGraph logic for managing state transitions between agents
- main.py           : Entry point for running the debate
- memory.py         : (Optional) Handles shared memory between rounds

How It Works:
-------------
1. Supervisor introduces a topic and initializes the state.
2. Agent 1 presents its argument.
3. Agent 2 responds with a counter-argument.
4. Supervisor evaluates the turn, provides feedback or scores.
5. The debate continues for N rounds.
6. Optionally, a winner is selected or a summary is generated.

Setup Instructions:
-------------------
1. Install dependencies:
   pip install -r ../../requirements.txt

2. Set environment variables:
   - OPENAI_API_KEY or GROQ_API_KEY

3. Run the debate:
   python main.py

Customization:
--------------
- Modify `agent1.py` and `agent2.py` for different personalities or expertise.
- Change debate topics in `main.py`.
- Tune LangGraph in `graph.py` for more/less debate rounds.
- Enable memory or scoring in `supervisor.py`.

Use Cases:
----------
- Simulating multi-agent decision making
- Opinion generation on controversial topics
- Comparative reasoning by LLMs
- Educational debate simulations

Dependencies:
-------------
- LangGraph
- LangChain
- OpenAI or Groq (for LLMs)
- dotenv (for env management)

Author:
-------
Harsha Vardhan Leabaka

