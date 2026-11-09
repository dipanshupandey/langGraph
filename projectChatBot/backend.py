from langgraph.graph import StateGraph,START,END
from typing import TypedDict, Annotated
from langchain_cohere import ChatCohere
from langchain_core.messages import BaseMessage,HumanMessage
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3
from dotenv import load_dotenv
# load_dotenv()  # load COHERE_API_KEY before the backend creates the model

class state(TypedDict):
    messages:Annotated[list[BaseMessage],add_messages]
model_name=	"command-a-03-2025"
model=ChatCohere(model=model_name,temperature=0.5)

def chatNode(state:TypedDict)->dict:
    messages=state['messages']
    result=model.invoke(messages)
    return {
        "messages":[result]
    }
graph= StateGraph(state)
graph.add_node("chatNode",chatNode)
graph.add_edge(START,"chatNode")
graph.add_edge("chatNode",END)
# bot=graph.compile(checkpointer=MemorySaver())
conn = sqlite3.connect(database="chatbot.db",check_same_thread=False)
checkpointer=SqliteSaver(conn=conn)
bot=graph.compile(checkpointer=checkpointer)

def retrieve_all_threads():
    all_threads = set()
    for checkpoint in checkpointer.list(None):
        all_threads.add(checkpoint.config['configurable']['thread_id'])
        # print(checkpoint.config)

    return list(all_threads)
# retrieve_all_threads()




