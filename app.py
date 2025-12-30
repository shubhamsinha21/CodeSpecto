import streamlit as st
from langchain_client import LangChainClient
from core.file_indexer import build_file_index
from core.code_parser import parse_code
from core.context_builder import build_context
from core.diff_engine import extract_diff, apply_patch
from core.security_scanner import scan_files

# ------------------- Page Setup ------------------- #
st.set_page_config(page_title="CodeSpecto", layout="wide")
st.markdown("<h1 style='color:#4B0082;'>🔍 CodeSpecto</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='color:#6A5ACD;'>AI-powered project intelligence for developers</h4>", unsafe_allow_html=True)

# ------------------- Session State ------------------- #
if "files" not in st.session_state:
    st.session_state.files = {}
if "patched_files" not in st.session_state:
    st.session_state.patched_files = {}
if "issues" not in st.session_state:
    st.session_state.issues = []
if "file_context" not in st.session_state:
    st.session_state.file_context = {}  # {file_name: context string}
if "file_messages" not in st.session_state:
    st.session_state.file_messages = {}  # {file_name: chat history}
if "analysis_results" not in st.session_state:
    st.session_state.analysis_results = {}  # {file_name: reply string}

# ------------------- Sidebar ------------------- #
with st.sidebar:
    st.markdown("<h3 style='color:#FF4500;'>📁 Upload Project Files</h3>", unsafe_allow_html=True)
    uploaded = st.file_uploader(
        "Upload files",
        accept_multiple_files=True,
        type=["py","js","ts","jsx","tsx","java","go","json","md"]
    )
    if uploaded:
        for f in uploaded:
            st.session_state.files[f.name] = f.read().decode("utf-8", errors="ignore")

    if st.session_state.files:
        st.markdown("<h3 style='color:#1E90FF;'>📂 Select File for Context</h3>", unsafe_allow_html=True)
        selected_file = st.selectbox(
            "Choose a file to continue discussion:",
            list(st.session_state.files.keys())
        )

    st.markdown("<h3 style='color:#32CD32;'>⚙️ Select Mode</h3>", unsafe_allow_html=True)
    mode = st.selectbox(
        "Select mode",
        ["General Guide","Debugger","Code Optimizer","Review Your Code","Security Scanner"]
    )

    analyse_btn = st.button("🔍 Analyse Project", help="Click to analyse your uploaded files in selected mode")

# ------------------- Analyse Logic ------------------- #
if analyse_btn and st.session_state.files:
    client = LangChainClient(mode)

    if mode == "Security Scanner":
        # Convert files into parsed dicts for scan_files
        parsed_index = [{"file_path": k, "content": v} for k, v in st.session_state.files.items()]
        with st.spinner("⚡ Analysing project files for security issues, please wait..."):
            issues = scan_files(parsed_index)
            st.session_state.issues = issues

        st.markdown("<h4>🚨 Security Issues Detected</h4>", unsafe_allow_html=True)
        if not issues:
            st.success("No critical security issues found 🎉")
        else:
            for i in issues:
                severity_color = {"HIGH":"#FF0000","MEDIUM":"#FFA500","LOW":"#00FF00"}.get(i["severity"],"#0000FF")
                st.markdown(
                    f"<span style='color:{severity_color}; font-weight:bold;'>[{i['severity']}]</span> "
                    f"{i['file']} → {i['issue']}",
                    unsafe_allow_html=True
                )

        if issues:
            security_context = "\n".join(
                f"{i['file']}: {i['issue']} ({i['severity']})" for i in issues
            )
            full_prompt = (
                "Security issues found in the project files:\n"
                f"{security_context}\n\n"
                "Suggest fixes with code diffs if possible."
            )
            with st.spinner("💡 Generating AI suggestions..."):
                reply = client.chat([{"role":"user","content":full_prompt}])
                diff = extract_diff(reply)
                st.markdown("<h4>💡 AI Suggested Fixes</h4>", unsafe_allow_html=True)
                st.markdown(reply)
                if diff:
                    st.markdown("<h4>🔧 Suggested Patch</h4>", unsafe_allow_html=True)
                    st.code(diff, language="diff")
                    st.session_state.patched_files["security_patch"] = apply_patch(
                        "\n".join(st.session_state.files.values()), diff
                    )

    else:
        file_content = st.session_state.files[selected_file]
        with st.spinner(f"⚡ Analysing {selected_file}, please wait..."):
            context = build_context([{"file_path": selected_file, "content": file_content}], f"Analyse {mode}")
            st.session_state.file_context[selected_file] = context

            if selected_file not in st.session_state.file_messages:
                st.session_state.file_messages[selected_file] = []

            full_prompt = f"{context}\n\nMode: {mode}"
            st.session_state.file_messages[selected_file].append({"role":"user","content":full_prompt})
            reply = client.chat(st.session_state.file_messages[selected_file])
            st.session_state.file_messages[selected_file].append({"role":"assistant","content":reply})

            # Save analysis result for UI display
            st.session_state.analysis_results[selected_file] = reply

# ------------------- Display AI Analysis for Selected File ------------------- #
if st.session_state.files and 'selected_file' in locals():
    if selected_file in st.session_state.analysis_results:
        with st.expander(f"💡 AI Analysis: {selected_file}", expanded=True):
            st.markdown(st.session_state.analysis_results[selected_file])
            # If diff exists, show suggested patch
            diff = extract_diff(st.session_state.analysis_results[selected_file])
            if diff:
                st.markdown("<h4>🔧 Suggested Patch</h4>", unsafe_allow_html=True)
                st.code(diff, language="diff")

# ------------------- Optional Chat (Stateful, Per-File) ------------------- #
if st.session_state.files and 'selected_file' in locals():
    st.markdown("<h4>💬 Optional Chat with AI</h4>", unsafe_allow_html=True)
    chat_input = st.text_input(f"Ask more about {selected_file}:")
    if chat_input:
        client = LangChainClient(mode)
        messages = st.session_state.file_messages.get(selected_file, [])
        full_prompt = f"{st.session_state.file_context[selected_file]}\n\nUser Query:\n{chat_input}"
        messages.append({"role":"user","content":full_prompt})
        with st.spinner("💡 AI is thinking..."):
            reply = client.chat(messages)
        messages.append({"role":"assistant","content":reply})
        st.session_state.file_messages[selected_file] = messages
        st.markdown(reply)
