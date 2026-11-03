from langgraph.graph import StateGraph,START,END
from typing import TypedDict, Annotated
from langchain_cohere import ChatCohere
from langchain_core.messages import BaseMessage,HumanMessage
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
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
bot=graph.compile(checkpointer=MemorySaver())



if __name__=="__main__":
    config={
    "configurable":{
        "thread_id":1
    }
}
    while True:
        message=input("Type here")
        if message not in ["break","quit","exit"]:
            response=bot.invoke({"messages":[HumanMessage(content=message)]},config=config)
            print(response["messages"][-1].content)
        else:
            break


