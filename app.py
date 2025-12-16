import streamlit as st
from langchain_community.document_loaders import Docx2txtLoader, PyPDFLoader
import os
import tempfile

st.set_page_config(page_title="AI CODE ASSISTANT", layout="wide")
st.title("AI CODE ASSISTANT")