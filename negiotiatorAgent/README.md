Project Title:
LLM-Powered Negotiator Agent (negiotiatorAgent)

Description:
This project is a simple simulation of a negotiation between two autonomous agents—an Optimist and a Skeptic. Each agent is powered by a language model and designed with different perspectives:

- The Optimist Agent tends to be open-minded and supportive of ideas.
- The Skeptic Agent is critical, questioning, and challenges proposals.

They exchange arguments, propose solutions, and attempt to reach a consensus or defend their viewpoints using LLMs. This is a stepping stone towards more complex agent debate, negotiation, or multi-agent orchestration systems.

Folder Structure:
negiotiatorAgent/
│
├── agent1.py             # Optimist agent definition
├── agent2.py             # Skeptic agent definition
├── main.py               # Script to initiate and run the negotiation
├── utils.py              # Shared functions/utilities
└── README.txt            # (This file)

Requirements:
- Python 3.10+
- langchain or similar LLM framework (depending on your implementation)
- An OpenAI-compatible LLM or local LLM support (e.g., Groq/Gemma/Unsloth/etc.)
- Optional: LangGraph or agent orchestration library (if used)

You can install common requirements with:
pip install -r requirements.txt
(Note: Create requirements.txt if not already present.)

How to Run:
1. Clone the repo:
   git clone https://github.com/lharsha2005/llm-aiAgents.git
   cd llm-aiAgents/negiotiatorAgent

2. Run the negotiation script:
   python main.py

3. You should see the exchange of dialogue between the two agents in your terminal.

Customization Ideas:
- Change the agent personalities in agent1.py and agent2.py.
- Use a different LLM backend (OpenAI, Groq, etc.)
- Add a supervisor or referee agent to score the arguments.
- Add memory or feedback loops to simulate learning behavior.

Use Cases:
- Multi-agent simulation research
- AI debate or philosophical discussion models
- Testing LLM prompt engineering and viewpoint simulation
- Foundation for negotiation/bargaining agents in decision-making systems

Author:
Harsha Vardhan Leabaka
GitHub: https://github.com/lharsha2005
