from State import State
from langgraph.types import Command

def debate(state: State)->State:
    if state["round"] > state["max_rounds"]:
        return Command(goto="sentiment")
    goto="agent_1" if state["round"] % 2 == 0 else "agent_2"
    return Command(goto=goto)