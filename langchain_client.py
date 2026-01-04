import os
import logging
from dotenv import load_dotenv
from typing import List, Dict

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class LangChainClient:
    def __init__(
        self,
        mode: str = "General Guide",
        model_name: str = "gemini-2.5-flash",
        temperature: float = 0.2,
    ):
        self.mode = mode

        self.prompts = {
            "General Guide": "You are an expert software assistant.",
            "Debugger": "You are an expert debugger. Provide suggestions and diffs as needed.",
            "Code Optimizer": "You are an expert code optimizer.",
            "Review Your Code": "You are an expert code reviewer with actionable feedback.",
            "Security Scanner": "You are a security expert for code security scanning."
        }

        self.system_prompt = self.prompts.get(mode, self.prompts["General Guide"])

        self.api_key = os.getenv("GOOGLE_API_KEY")
        self.model = None

        if not self.api_key:
            logging.error("GOOGLE_API_KEY is missing.")
            return

        try:
            self.model = ChatGoogleGenerativeAI(
                model=model_name,
                temperature=temperature,
                google_api_key=self.api_key
            )
        except Exception as e:
            logging.exception("Failed to initialize Gemini model", exc_info=e)
            self.model = None

    def chat(self, messages: List[Dict[str, str]]) -> str:
        if not self.model:
            return (
                "⚠️ **Gemini API key is missing or invalid.**\n\n"
                "Please configure the API key and try again."
            )

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
                prompt_msgs.append(AIMessage(content=content))

        try:
            result = self.model.invoke(prompt_msgs)
            return getattr(result, "content", str(result))

        except Exception as e:
            error_msg = str(e).lower()
            logging.exception("Gemini invocation failed", exc_info=e)

            # ✅ Gemini free-tier / quota handling
            if (
                "quota" in error_msg
                or "resource_exhausted" in error_msg
                or "429" in error_msg
                or "rate limit" in error_msg
            ):
                return (
                    "🚧 **Gemini free tier limit reached**\n\n"
                    "Please wait for some time and try again later 🙂"
                )

            # Generic safe message
            return (
                "❌ **Something went wrong while processing your request.**\n\n"
                "Please try again later."
            )
