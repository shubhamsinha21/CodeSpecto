import streamlit as st
from langchain_community.document_loaders import Docx2txtLoader, PyPDFLoader
import os
import tempfile
from langchain_client import LangChainClient

st.set_page_config(page_title="AI CODE ASSISTANT", layout="wide")

# session state -->
if "message" not in st.session_state:
    st.session_state.message = []
    
if "mode" not in st.session_state:
        st.session_state.mode = None
    
if "uploaded_texts" not in st.session_state:
        st.session_state.uploaded_texts = {} # filename-> extracted text
        
st.title("🤖 AI CODE ASSISTANT")

# sidebar upload -->
st.sidebar.header("📁 Project Files")
uploaded_files = st.sidebar.file_uploader("Upload your project files here", 
    accept_multiple_files=True,
    type=["pdf", "docx", "txt", "md", "csv", "json", "go", "js", "py", 
          "tsx", "ts", "jsx", "java", "c", "cpp", "html", "css"
          ]
)

# sidebar mode dropdown -->
st.sidebar.header("⚙️ Select Mode")
mode = st.sidebar.selectbox(
    "Choose a mode for interaction (required):",
    [
        "General Guide",
        "Debugger",
        "Code Optimizer",
        "Code Explainer",
        "Project Builder",
        "Review Your Code",
        "Documentation Generator",
        "Code Generator",
    ],
    index=0,
)

st.session_state.mode = mode

LC = LangChainClient(mode=st.session_state.mode) # instance of the onstructor class
st.caption(f"**🟢 Assistant is running in :** {mode} mode")


def extract(file): 
    """ 
    Creating the extract function suitable for handling different file formats (csv/ doc/ html, etc)
    """

        

# check for files uploaded
if uploaded_files:
    for f in uploaded_files:
        if f.name not in st.session_state.uploaded_texts:
            try:
                st.session_state.uploaded_texts[f.name] = extract(f)
            except Exception as e:
                st.session_state.uploaded_texts[f.name] = "Could not able to read the file"

    # success msg when file gets uploaded
    st.sidebar.success(f"{len(st.session_state.uploaded_textx)} file(s) ready for analysis !")
