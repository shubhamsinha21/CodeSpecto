# 🔍 CodeSpecto

**AI-powered Project Intelligence for Developers**

CodeSpecto is an advanced AI code assistant designed for developers to analyze, debug, optimize, review, and secure their code projects. Built using **Streamlit**, **LangChain**, and **Google Gemini AI**, it provides actionable insights, code suggestions, and security recommendations in an interactive and stateful interface.


## 🚀 Features

- **Multi-Mode Analysis**
  - **General Guide**: Get guidance and suggestions on your project.
  - **Debugger**: Identify bugs in code files automatically.
  - **Code Optimizer**: Receive optimization suggestions for better performance and readability.
  - **Review Your Code**: AI-based code review with detailed suggestions.
  - **Security Scanner**: Detect potential security vulnerabilities and suggest fixes.

- **File-Aware Context**
  - Analyze multiple files at once.
  - Preserve context for stateful discussions per file.
  - Ask follow-up questions about specific files without losing previous analysis.

- **Diff & Patch Suggestions**
  - Highlight suggested changes.
  - Apply AI-generated patches directly.

- **Interactive Chat**
  - Stateful chat interface with AI.
  - Optional queries after initial analysis, context preserved.

- **Beautiful & Responsive UI**
  - Enhanced color-coded UI.
  - Loading spinners and status messages during analysis.
  - Expander sections for detailed AI insights.

- **Supported File Types**
  - Python (`.py`), JavaScript (`.js`), TypeScript (`.ts`, `.tsx`, `.jsx`)
  - Java (`.java`), Go (`.go`), JSON (`.json`), Markdown (`.md`)

  
## 📂 Architecture & File Structure

CodeSpecto/
- app.py # Main Streamlit interface and UI
- langchain_client.py # LangChain + Google Gemini AI integration
- requirements.txt # Python dependencies
- core/
  - file_indexer.py # Index and manage uploaded files
  - code_parser.py # Parse code and extract snippets
  - context_builder.py # Build AI context per file
  - diff_engine.py # Extract/apply AI suggested diffs
  - security_scanner.py # Scan files for security issues
  - README.md # Project documentation


## ⚙️ Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/CodeSpecto.git
cd CodeSpecto
```

2. Create a virtual environment and activate:
```bash
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
.venv\Scripts\activate      # Windows
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Create .env file and add your Google Gemini API key:
```bash
GOOGLE_API_KEY=your_api_key_here
```

### Running the project
```bash 
streamlit run app.py
```

- Upload your project files in the sidebar.

- Select the mode (Debugger, Code Optimizer, Security Scanner, etc.).

- Click "Analyse Project".

- View AI analysis, suggestions, and optional patch diffs.

- Use the optional chat box to ask follow-up questions.


## 🧠 How It Works (Technical Overview)

1. File Indexing

- Uploaded files are read and stored in session state.
- Files are parsed into snippets for AI processing.

2. Context Building

- ontext per file is built based on keywords and mode.
- Ensures AI understands which file/code block to reference.

3. LangChain + Google Gemini AI

- Different system prompts based on selected mode.
- Messages include previous AI responses for context-preserving chat.

4. Diff & Patch Engine

- AI suggestions are parsed for potential code changes.
- Suggested patches can be viewed or applied.

5. Security Scanning

- Static analysis-like checks for HIGH/MEDIUM/LOW severity issues.
- AI generates possible fixes with code diffs.


## 🎨 UI / UX Enhancements

**Stateful Session**: Context preserved for continuous interaction.

**Color-Coded Analysis**: Severity of issues shown with intuitive colors.

**Loading Spinner**: Shows progress during analysis.

**Expandable Sections**: AI insights and patches in expandable sections for better readability.


## Best Practices & Notes

- Maximum file size per upload: 200MB.
- Context preserved per session, ensure to continue discussions in the same session.
- Google Gemini API quota limits apply — free tier allows limited requests daily.
- AI suggestions should be reviewed before applying in production.


## 🛠️ Tech Stack

**Frontend / UI**: Streamlit
**Backend / AI Client**: LangChain, Google Gemini AI
**Language Parsing & Diffing**: Python
**Environment Management**: python-dotenv

## 📄 License

MIT License © [Shubham Sinha]

## 🔗 References

- LangChain Documentation

- Google Gemini AI

- Streamlit Documentation

