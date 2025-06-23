from typing import TypedDict
from agent1 import run_agent1
from agent2 import run_agent2
from voterAgent import voter_agent
from langgraph.graph import StateGraph

class State(TypedDict):
    messages: list[str]
    question: str
    answer: str
    round: int
    max_rounds: int

def debate_router(state: State) -> str:
    if state["round"] >= state["max_rounds"]:
        return "voter"
    return "agent_1" if state["round"] % 2 == 0 else "agent_2"


builder = StateGraph(State)

builder.add_node("agent_1", run_agent1)
builder.add_node("agent_2", run_agent2)
builder.add_node("voter", voter_agent)

builder.add_conditional_edges("agent_1", debate_router)
builder.add_conditional_edges("agent_2", debate_router)

builder.set_entry_point("agent_1")
builder.set_finish_point("voter")

graph=builder.compile()

msg={
    "question": "How should I invest 100,000 rupees",
    "messages": [],
    "round": 0,
    "max_rounds": 8,
}

output=graph.invoke(msg)

print("Full Debate:")
for i in range(len(output["messages"])):
    print(output["messages"][i])
    print()

print("\nFinal Decision:")
print(output["answer"])
