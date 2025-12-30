import streamlit as st
import tempfile, os

from langchain_client import LangChainClient
from core.file_indexer import build_file_index
from core.code_parser import parse_code
from core.context_builder import build_context
from core.diff_engine import extract_diff, apply_patch

st.set_page_config("CodeSpecto", layout="wide")
st.title("🔍 CodeSpecto")
st.caption("AI-powered repository intelligence")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "files" not in st.session_state:
    st.session_state.files = {}

st.sidebar.header("📁 Upload Project Files")
uploaded = st.sidebar.file_uploader(
    "Upload files",
    accept_multiple_files=True,
    type=["py","js","ts","jsx","tsx","java","go","json","md"]
)

if uploaded:
    for f in uploaded:
        st.session_state.files[f.name] = f.read().decode("utf-8", errors="ignore")

st.sidebar.header("⚙️ Mode")
mode = st.sidebar.selectbox(
    "Select mode",
    ["General Guide","Debugger","Code Optimizer","Review Your Code"]
)

client = LangChainClient(mode)

prompt = st.chat_input("Ask CodeSpecto...")

if prompt:
    file_index = build_file_index(st.session_state.files)
    parsed = [parse_code(f) for f in file_index]
    context = build_context(parsed, prompt)

    full_prompt = f"{context}\n\nUser Query:\n{prompt}"

    st.session_state.messages.append({"role":"user","content":full_prompt})
    reply = client.chat(st.session_state.messages)

    diff = extract_diff(reply)

    with st.chat_message("assistant"):
        st.markdown(reply)
        if diff:
            st.subheader("🔧 Suggested Patch")
            st.code(diff, language="diff")

    st.session_state.messages.append({"role":"assistant","content":reply})
