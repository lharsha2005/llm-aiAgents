from typing import TypedDict, Literal
from typing_extensions import Annotated
from pydantic import BaseModel, Field
from langgraph.graph import add_messages
from langchain_groq import ChatGroq
from langchain_tavily import TavilySearch
from langchain_experimental.utilities import PythonREPL
from langgraph.graph import StateGraph,START,END
from langgraph.types import Command
from langchain.tools import tool
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent
from pprint import pprint
import os
from dotenv import load_dotenv

#misc
class State(TypedDict):
    messages:Annotated[list,add_messages]

#init
load_dotenv()
TAVILY_API_KEY=os.getenv("TAVILY_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

llm= ChatGroq(model="llama-3.3-70b-versatile",temperature=0.7)
repl=PythonREPL()
tavilyTool=TavilySearch(max_results=2)
tools=[repl,tavilyTool]

@tool
def run_python_code(code: str) -> str:
    """Execute Python code and return the result."""
    return repl.run(code)
#supervisor
system_prompt=('''You are a workflow supervisor managing a team of three agents: Prompt Enhancer, Researcher, and Coder. Your role is to direct the flow of tasks by selecting the next agent based on the current stage of the workflow. For each task, provide a clear rationale for your choice, ensuring that the workflow progresses logically, efficiently, and toward a timely completion.

**Team Members**:
1. Enhancer: Use prompt enhancer as the first preference, to Focuse on clarifying vague or incomplete user queries, improving their quality, and ensuring they are well-defined before further processing.
2. Researcher: Specializes in gathering information.
3. Coder: Handles technical tasks related to caluclation, coding, data analysis, and problem-solving, ensuring the correct implementation of solutions.

**Responsibilities**:
1. Carefully review each user request and evaluate agent responses for relevance and completeness.
2. Continuously route tasks to the next best-suited agent if needed.
3. Ensure the workflow progresses efficiently, without terminating until the task is fully resolved.

Your goal is to maximize accuracy and effectiveness by leveraging each agent's unique expertise while ensuring smooth workflow execution.
''')

class Supervisor(BaseModel):
    name: Literal["researcher","enhancer","coder"]=Field(
        description="Specifies the next worker in the pipeline: "
                    "'enhancer' for enhancing the user prompt if it is unclear or vague, "
                    "'researcher' for additional information gathering, "
                    "'coder' for solving technical or numbers related problems or code-related problems."
    )

    reson: str=Field(
        description="The reason for the decision, providing context on why a particular worker was chosen."
    )

def supervisor(state: State):
    """
    Supervisor node for routing tasks based on the current state and LLM response.
    Args:
        state (MessagesState): The current state containing message history.
    Returns:
        Command: A command indicating the next state or action.
    """
    msg=[{
        "role":"system",
        "content":system_prompt
    }]+state["messages"]

    response=llm.with_structured_output(Supervisor).invoke(msg)

    goto=response.name
    reson=response.reson 

    print(f"From: Supervisor->{goto}")
    return Command(
        update={
            "messages":[HumanMessage(content=reson,name="supervisor")]
        },
        goto=goto
    )

#enhance
def enhace(state: State):
    """
    Enhancer node for refining and clarifying user inputs.

    Args:
        state (MessagesState): The current state containing the conversation history.

    Returns:
        Command: A command to update the state with the enhanced query and route back to the supervisor.
    """
    prompt=(
        "You are an advanced query enhancer. Your task is to:\n"
        "Don't ask anything to the user, select the most appropriate prompt"
        "1. Clarify and refine user inputs.\n"
        "2. Identify any ambiguities in the query.\n"
        "3. Generate a more precise and actionable version of the original request.\n"
    )

    msg=[{
        "role":"system",
        "content":prompt
    }]+state["messages"]

    response=llm.invoke(msg)
    goto="supervisor"

    if goto == "FINISH" or goto == END:
        goto = END 
        print("Transitioning to END")
    else:
        print(f"From: Enhancer->Supervisor")

    return Command(
        update={
            "messages":[HumanMessage(content=response.content,name="enhancer")]
        },
        goto="supervisor"
    )

#researcher
def researcher(state: State):
    """
    Research node for leveraging a ReAct agent to process research-related tasks.

    Args:
        state (MessagesState): The current state containing the conversation history.

    Returns:
        Command: A command to update the state with the research results and route to the validator.
    """

    agent=create_react_agent(llm,tools=[tavilyTool],prompt="You are a researcher. Focus on gathering information and generating content. Do not perform any other tasks")
    response=agent.invoke(state)
    print(f"From: Researcher->Validator")
    return Command(
        update={
            "messages":[HumanMessage(content=response["messages"][-1].content,name="researcher")]
        },
        goto="validator"
    )

#coder
def coder(state: State):
    """
    Coder node for leveraging a ReAct agent to process analyzing, solving math questions, and executing code.

    Args:
        state (MessagesState): The current state containing the conversation history.

    Returns:
        Command: A command to update the state with the research results and route to the validator.
    """
    agent=create_react_agent(llm,tools=[run_python_code],prompt=(
            "You are a coder and analyst. Focus on mathematical caluclations, analyzing, solving math questions, "
            "and executing code. Handle technical problem-solving and data tasks."
        ))
    response=agent.invoke(state)
    print(f"From: Coder->Validator")
    return Command(
        update={
            "messages":[HumanMessage(content=response["messages"][-1].content, name="coder")]
        },
        goto="validator"
    )

#validator
valid_prompt=system_prompt = '''
You are a workflow validator. Your task is to ensure the quality of the workflow. Specifically, you must:
- Review the user's question (the first message in the workflow).
- Review the answer (the last message in the workflow).
- If the answer satisfactorily addresses the question, signal to end the workflow.
- If the answer is inappropriate or incomplete, signal to route back to the supervisor for re-evaluation or further refinement.
Ensure that the question and answer match logically and the workflow can be concluded or continued based on this evaluation.

Routing Guidelines:
1. 'supervisor' Agent: For unclear or vague state messages.
2. Respond with 'FINISH' to end the workflow.
'''
class Validator(BaseModel):
    next: Literal["supervisor", "FINISH"] = Field(
        description="Specifies the next worker in the pipeline: 'supervisor' to continue or 'FINISH' to terminate."
    )
    reason: str = Field(
        description="The reason for the decision."
    )

def validator(state: State)-> Command[Literal["supervisor", "__end__"]]:
    """
    Validator node for checking if the question and the answer are appropriate.

    Args:
        state (MessagesState): The current state containing message history.

    Returns:
        Command: A command indicating whether to route back to the supervisor or end the workflow.
    """
    user_question = state["messages"][0].content
    agent_answer = state["messages"][-1].content

    msg = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_question},
        {"role": "assistant", "content": agent_answer},
    ]

    responce=llm.with_structured_output(Validator).invoke(msg)

    goto=responce.next

    if goto == "FINISH" or goto == END:
        goto = END  
        print("Transitioning to END")  
    else:
        print(f"Current Node: Validator -> Goto: Supervisor") 

    return Command(
        update={
            "messages":[HumanMessage(content=responce.reason, name="validator")]
        },
        goto=responce.next
    )

#graph
workflow=StateGraph(State)
workflow.add_node("supervisor",supervisor)
workflow.add_node("coder",coder)
workflow.add_node("enhancer",enhace)
workflow.add_node("researcher",researcher)
workflow.add_node("validator",validator)
workflow.add_edge(START, "supervisor")
workflow.add_edge("enhancer",END)
workflow.add_edge("validator",END)

graph=workflow.compile()

#run
input={
    "messages": [
        {
            "role": "user",
            "content": "give me how many A's present in a string of AVYGABAAHKJHDAAAAUHBU  ?"
        }
    ]
}

for output in graph.stream(input):
    for key,value in output.items():
        if value is None:
            continue
        last_message = value.get("messages", [])[-1] if "messages" in value else None
        if last_message:
            pprint(f"Output from node '{key}':")
            pprint(last_message, indent=2, width=80, depth=None)
            print()
