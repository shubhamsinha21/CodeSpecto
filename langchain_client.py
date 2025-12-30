import os
import logging
from dotenv import load_dotenv
from typing import List, Dict

# Correct import from the google genai integration package
from langchain_google_genai import ChatGoogleGenerativeAI  
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

load_dotenv()

# ------------------- Logging Setup ------------------- #
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class LangChainClient:
    """
    A client for interacting with Google Gemini / Google Generative AI
    using the LangChain integration (langchain-google-genai).
    """

    def __init__(
        self,
        mode: str = "General Guide",
        model_name: str = "gemini-2.5-flash",
        temperature: float = 0.2,
    ):
        """
        Initializes the LangChainClient with the given mode and model options.

        Args:
            mode (str): LLM assistant mode (e.g., "Debugger", "Review Your Code").
            model_name (str): Google Gemini model name.
            temperature (float): Sampling temperature for the model.
        """
        self.mode = mode

        # Prompts based on the chosen mode
        self.prompts = {
            "General Guide": "You are an expert software assistant.",
            "Debugger": "You are an expert debugger. Provide suggestions and diffs as needed.",
            "Code Optimizer": "You are an expert code optimizer.",
            "Review Your Code": "You are an expert code reviewer with actionable feedback.",
            "Security Scanner": "You are a security expert for code security scanning."
        }
        self.system_prompt = self.prompts.get(mode, self.prompts["General Guide"])

        # API key must be present
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY environment variable not set.")

        # Create the model instance
        self.model = ChatGoogleGenerativeAI(
            model=model_name,
            temperature=temperature,
            google_api_key=api_key
        )

    def chat(self, messages: List[Dict[str, str]]) -> str:
        """
        Send messages to the Google Gemini LLM via LangChain integration,
        and get the textual response.

        Args:
            messages (List[Dict[str,str]]): List of dict messages with role/content.

        Returns:
            str: The assistant's text response.
        """
        # Build LangChain message list with correct types
        prompt_msgs = [SystemMessage(content=self.system_prompt)]

        for m in messages:
            role = m.get("role", "")
            content = m.get("content", "")
            if role == "user":
                prompt_msgs.append(HumanMessage(content=content))
            elif role == "assistant":
                prompt_msgs.append(AIMessage(content=content))
            elif role == "system":
                prompt_msgs.append(SystemMessage(content=content))
            else:
                logging.warning(f"Unhandled role '{role}', treating as assistant.")
                prompt_msgs.append(AIMessage(content=content))

        # Invoke the model
        result = self.model.invoke(prompt_msgs)

        # Extract text content
        return getattr(result, "content", str(result))
