from langgraph.graph import StateGraph,START,END
from State import State


from ocrAgent import run_ocr
from supervisor import supervisor
from queryAgent import run_query
from VisionAgent import vision

workflow=StateGraph(State)
workflow.add_node("ocr",run_ocr)#using paddleocr
workflow.add_node("ocr",vision)#using llm
workflow.add_node("supervisor",supervisor)
workflow.add_node("query",run_query)

workflow.add_edge(START,"supervisor")
workflow.add_edge("query",END)

graph=workflow.compile()

# msg = {
#     "question": "What documents are required to open an account?",
#     "img_path": None,
#     "ocr_text": None,
#     "answer": None
# }


# res=graph.invoke(msg)
# print()
# print("Final Answer:", res["answer"])
