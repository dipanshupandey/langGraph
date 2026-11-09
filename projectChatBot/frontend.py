import uuid

import streamlit as st
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage

load_dotenv()  # load COHERE_API_KEY before the backend creates the model

from backend import bot,retrieve_all_threads  # the LangGraph chatbot (import after load_dotenv)


# ---------- Helper functions ----------

def generate_thread_id():
    # A unique id per chat; LangGraph uses it to keep each chat's memory separate
    return str(uuid.uuid4())


def get_messages(thread_id):
    # Read a chat's saved messages from the LangGraph checkpointer
    config = {"configurable": {"thread_id": thread_id}}
    state = bot.get_state(config)
    return state.values.get("messages", [])


def messages_to_history(messages):
    # Convert LangChain messages into the {"role", "content"} dicts shown on screen
    history = []
    for msg in messages:
        role = "user" if isinstance(msg, HumanMessage) else "assistant"
        history.append({"role": role, "content": msg.content})
    return history


def reset_chat():
    # "New Chat" button: start a fresh thread with an empty history
    new_id = generate_thread_id()
    st.session_state["thread_id"] = new_id
    st.session_state["history"] = []
    st.session_state["thread_list"].append(new_id)


def switch_chat(thread_id):
    # Sidebar chat button: make that thread active and reload its messages
    st.session_state["thread_id"] = thread_id
    st.session_state["history"] = messages_to_history(get_messages(thread_id))


# ---------- Session state (kept across reruns, lost on page refresh) ----------

if "thread_id" not in st.session_state:
    st.session_state["thread_id"] = generate_thread_id()  # the active chat
if "history" not in st.session_state:
    st.session_state["history"] = []  # messages shown on screen
if "thread_list" not in st.session_state:
    st.session_state["thread_list"] = retrieve_all_threads()
# Make sure the current (possibly brand-new) chat is also in the sidebar
if st.session_state["thread_id"] not in st.session_state["thread_list"]:
    st.session_state["thread_list"].append(st.session_state["thread_id"])

# ---------- Sidebar: chat list ----------

st.sidebar.title("Chats")
st.sidebar.button("New Chat", on_click=reset_chat)
for thread_id in st.session_state["thread_list"]:
    st.sidebar.button(thread_id, on_click=switch_chat, args=(thread_id,))


# ---------- Main area: conversation ----------

st.title("Chatbot")

# Tells LangGraph which chat's memory to use
config = {"configurable": {"thread_id": st.session_state["thread_id"]}}

# Show earlier messages (Streamlit reruns this script on every interaction)
for message in st.session_state["history"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle a new message from the user
user_input = st.chat_input("Type here")
if user_input:
    st.session_state["history"].append({"role": "user", "content": user_input})
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

    st.session_state["history"].append({"role": "assistant", "content": reply})
