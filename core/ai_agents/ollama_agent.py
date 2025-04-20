# core/ai_agents/ollama_agent.py
from langchain.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

class OllamaAgent:
    def __init__(self):
        self.llm = Ollama(model="codellama")

    def generate_tests(self, code: str):
        prompt = PromptTemplate.from_template(
            "Write hypothesis-style tests for the following code:\n\n{code}"
        )
        chain = LLMChain(llm=self.llm, prompt=prompt)
        return chain.run(code=code)

    def explain(self, code: str):
        prompt = PromptTemplate.from_template(
            "Explain any vulnerabilities in the following code:\n\n{code}"
        )
        chain = LLMChain(llm=self.llm, prompt=prompt)
        return chain.run(code=code)
