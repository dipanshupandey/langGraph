import uuid

import streamlit as st
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage

load_dotenv()  # load COHERE_API_KEY before the backend creates the model

from backend import bot

st.title("Chatbot")

# One thread_id per browser session, so each chat has its own memory
if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())
if "history" not in st.session_state:
    st.session_state.history = []

config = {"configurable": {"thread_id": st.session_state.thread_id}}

# Show earlier messages (Streamlit reruns this script on every interaction)
for message in st.session_state.history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_input = st.chat_input("Type here")
if user_input:
    st.session_state.history.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        stream = bot.stream(
            {"messages": [HumanMessage(content=user_input)]},
            config=config,
            stream_mode="messages",
        )
        # write_stream shows each chunk as it arrives and returns the full reply
        reply = st.write_stream(chunk.content for chunk, metadata in stream)

    st.session_state.history.append({"role": "assistant", "content": reply})
