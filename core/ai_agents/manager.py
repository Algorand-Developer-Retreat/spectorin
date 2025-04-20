# core/ai_agents/manager.py
from core.ai_agents.ollama_agent import OllamaAgent

class AIAgentManager:
    def __init__(self):
        self.agent = OllamaAgent()

    def generate_tests(self, code: str):
        return self.agent.generate_tests(code)

    def explain_vulnerability(self, code: str):
        return self.agent.explain(code)
