from langgraph.graph import StateGraph,START,END
from langgraph.types import Command
from typing import TypedDict
from typing_extensions import Annotated

from ocrAgent import run_ocr
from paserAgent import run_paser
from queryAgent import run_qury
from checkerAgent import run_checker
from supervisor import supervisor

class State(TypedDict):
    img_path: str
    ocr_text: str
    check: bool
    corrected_data: dict
    question: str
    answer: str
    goto: str

def ocr_node(state: State) -> State:
    text = run_ocr(state['img_path'])
    return Command(
        update={"ocr_text": text},
        goto="supervisor"
    )

def paser_node(state: State) -> State:
    result = run_paser(state["ocr_text"])
    return Command(
        update={"corrected_data": result.content},
        goto="supervisor"
    )

def query_node(state: State) -> State:
    result = run_qury(state["question"], state["corrected_data"])
    return Command(
        update={"answer": result.content},
        goto=END
    )

def checker_node(state: State)->State:
    result=run_checker(state["ocr_text"],state["question"])
    return Command(
        update={"check": result[1]},
        goto=result[0]
    )

workflow=StateGraph(State)
workflow.add_node("ocr",ocr_node)
workflow.add_node("paser",paser_node)
workflow.add_node("query",query_node)
workflow.add_node("supervisor",supervisor)
workflow.add_node("checker",checker_node)

workflow.add_edge(START,"supervisor")
workflow.add_edge("query",END)
workflow.add_edge("checker",END)

graph=workflow.compile()

# if __name__ == "__main__":
#     output = graph.invoke({
#         "img_path": "bank.png",
#         "question": "give transations on 30/05/2020",
#         "answer": "Conditions not stisfied",
#     })
#     print()
#     print("Final Answer:", output["answer"])
