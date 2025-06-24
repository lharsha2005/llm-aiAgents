from State import State
from langgraph.types import Command
from langgraph.graph import END

def user(state: State)->State:
    print("**debate**:")
    print("-"*140)
    for i,message in enumerate(state["history"]):
        print(message)
        print()
    print("-"*140)
    print("\n**negotiator data**")
    print("-"*140)
    print(state["negotiator_data"])
    print("-"*140)

    goto="supervisor"
    feedback=input("User:")
    if feedback=='exit':
        goto=END
    print("user->supervisor")
    return Command(update={"feedback":feedback,"debate_flag":False},goto=goto)
