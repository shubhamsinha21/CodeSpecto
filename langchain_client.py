from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

class LangChainClient:
    # constructor
    def __init__(self, mode="General Guide"):
        role_prompts = {
            "Code Generator": " You are an expert code generator. Generate code snippets based on user requirements with best practices in mind.",
            "Debugger": " You are an expert debugger. Help identify and fix bugs in the provided code snippets.",
            "Code Optimizer": " You are an expert code optimizer. Suggest improvements to enhance code performance and readability.",
            "Code Explainer": " You are an expert code explainer. Provide clear explanations of code snippets to help users understand their functionality.",
            "Project Builder": " You are an expert project builder. Assist users in structuring and organizing their code projects effectively.",
            "Review Your Code": " You are an expert code reviewer. Provide constructive feedback on code quality, style, and best practices.",
            "Documentation Generator": " You are an expert documentation generator. Create comprehensive and clear documentation for codebases.",
            "General Guide": " You are a general coding assistant. Provide helpful guidance and support for various coding-related queries.",
        }
        
        self.system_prompt = role_prompts.get(mode, role_prompts["General Guide"])
        
        self.model = ChatGoogleGenerativeAI(
            model = "gemini-1.5-flash",
            temperature = 0.2,
            google_api_key = os.getenv("GOOGLE_API_KEY")
        )
        
# constructor simply loads the llm model and creates sytsem prompt based on user behavior

   
        
    