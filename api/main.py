# api/main.py
from fastapi import FastAPI
from core.ai_agents.manager import AIAgentManager

app = FastAPI()
agent = AIAgentManager()

@app.post("/analyze")
def analyze_code(code: str):
    return {"explanation": agent.explain_vulnerability(code)}
