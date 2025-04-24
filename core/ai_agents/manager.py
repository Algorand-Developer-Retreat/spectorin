# core/ai_agents/manager.py
from core.ai_agents.ollama_agent import OllamaAgent
from typing import List, Dict, Any

class AIAgentManager:
    def __init__(self, memory_efficient: bool = False):
        self.agent = OllamaAgent(memory_efficient=memory_efficient)

    def generate_recommendations(self, code: str, language: str, issues: List[Dict[str, Any]]) -> List[str]:
        """Generate recommendations based on code analysis results"""
        return self.agent.generate_recommendations(code, language, issues)

    def generate_tests(self, code: str):
        return self.agent.generate_tests(code)

    def explain_vulnerability(self, code: str):
        return self.agent.explain(code)
