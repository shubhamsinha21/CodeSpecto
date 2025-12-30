from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from dotenv import load_dotenv
import os

load_dotenv()

class LangChainClient:
    def __init__(self, mode="General Guide"):
        self.prompts = {
            "Debugger": (
                "You are an expert debugger. "
                "Return a unified diff inside ```diff``` blocks. "
                "After diff, give a short explanation."
            ),
            "Code Optimizer": (
                "You are an expert code optimizer. "
                "Always return optimized code as a unified diff."
            ),
            "Review Your Code": (
                "You are an expert code reviewer. "
                "List issues with severity and suggestions."
            ),
            "Documentation Generator": (
                "Generate clean technical documentation."
            ),
            "General Guide": (
                "You are a senior software engineer helping with code."
            )
        }

        self.system_prompt = self.prompts.get(mode, self.prompts["General Guide"])

        self.model = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            temperature=0.2,
            google_api_key=os.getenv("GOOGLE_API_KEY")
        )

    def chat(self, messages):
        prompt = [SystemMessage(content=self.system_prompt)]

        for m in messages:
            if m["role"] == "user":
                prompt.append(HumanMessage(content=m["content"]))
            else:
                prompt.append(AIMessage(content=m["content"]))

        response = self.model.invoke(prompt)
        return response.content
