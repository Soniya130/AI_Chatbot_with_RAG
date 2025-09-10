import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="langchain_core.globals")

import streamlit as st
import os
from langchain.globals import set_verbose
set_verbose(False)

from models.llm import get_chat_model
from utils.websearch_utils import web_search
from utils.rag_utils import build_vector_store, retrieve_answer   # ✅ use build_vector_store


# ✅ Cache the LLM so it loads only once
@st.cache_resource
def get_llm():
    return get_chat_model()


# ✅ Cache the vector store so embeddings load only once
@st.cache_resource
def get_vector_store():
    return build_vector_store(path="vector_store")   # ✅ FIXED

vector_store = get_vector_store()
llm = get_llm()


def chat_page():
    st.title("🤖 AI ChatBot with RAG + Web Search")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    mode = st.radio("Choose Response Mode:", ["Concise", "Detailed"], horizontal=True)

    # Show chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # User input
    if prompt := st.chat_input("Type your message here..."):
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                rag_results = retrieve_answer(prompt, vector_store, llm)
                response = rag_results if isinstance(rag_results, str) else rag_results.content
                st.markdown(response)

        st.session_state.messages.append({"role": "assistant", "content": response})


# ✅ Entry point
if __name__ == "__main__":
    chat_page()
