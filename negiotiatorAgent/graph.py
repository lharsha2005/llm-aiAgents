from langgraph.graph import StateGraph,START,END
from State import State

from supervisor import supervisor
from ocrAgent import run_ocr
from extractorAgent import extractor
from debateAgent import debate
from agent1 import run_agent1
from agent2 import run_agent2
from negotiatorAgent import negotiator
from userAgent import user

workflow=StateGraph(State)
workflow.add_node("supervisor",supervisor)
workflow.add_node("ocr",run_ocr)
workflow.add_node("extractor",extractor)
workflow.add_node("debate",debate)
workflow.add_node("agent_1",run_agent1)
workflow.add_node("agent_2",run_agent2)
workflow.add_node("negotiatior",negotiator)
workflow.add_node("user",user)

workflow.add_edge(START,"supervisor")
workflow.add_edge("user",END)

graph=workflow.compile()

msg = {
    "img_path": "2.png",
    "ocr_data": "",
    "extractor_data": "",
    "history": [],
    "feedback": "",
    "round": 0,
    "max_rounds": 4,
    "debate_flag": False,
    "negotiator_flag": False
}


res=graph.invoke(msg)
print()
print("Final Answer:", res["negotiator_data"])
