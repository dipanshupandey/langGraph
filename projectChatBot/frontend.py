import uuid

import streamlit as st
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage

load_dotenv()  # load COHERE_API_KEY before the backend creates the model

from backend import bot  


def get_text(content):
    # Some models return a list of blocks; keep only the text block(s)
    if isinstance(content, str):
        return content
    return "".join(item["text"] for item in content if item.get("type") == "text")


st.set_page_config(page_title="Chatbot", page_icon="💬")
st.title("Chatbot")

# One thread_id per browser session, so each chat has its own memory
if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())
if "history" not in st.session_state:
    st.session_state.history = []  # messages shown on screen: {"role", "content"}

config = {"configurable": {"thread_id": st.session_state.thread_id}}



# Redraw earlier messages (Streamlit reruns this script on every interaction)
for message in st.session_state.history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_input = st.chat_input("Type here")
if user_input:
    st.session_state.history.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        try:
            with st.spinner("Thinking..."):
                response = bot.invoke(
                    {"messages": [HumanMessage(content=user_input)]},
                    config=config,
                )
            reply = get_text(response["messages"][-1].content)
            st.markdown(reply)
            st.session_state.history.append({"role": "assistant", "content": reply})
        except Exception as e:
            st.error(f"Something went wrong: {e}")
