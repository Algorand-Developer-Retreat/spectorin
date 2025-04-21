# api/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import re

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for demo
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AnalyzeRequest(BaseModel):
    code: str
    language: str

class Issue(BaseModel):
    severity: str
    message: str
    line: Optional[int] = None

class AnalyzeResponse(BaseModel):
    score: int
    issues: List[Issue]
    recommendations: List[str]
    summary: str
    error: Optional[str] = None

@app.get("/")
def read_root():
    return {"status": "API is running"}

@app.post("/api/analyze")
def analyze(request: AnalyzeRequest):
    code = request.code
    language = request.language.lower()
    
    # Simple demo analyzers
    issues = []
    recommendations = []
    
    if language == "solidity":
        # Check for reentrancy
        if ".call{value:" in code:
            issues.append({"severity": "high", "message": "Potential reentrancy vulnerability", "line": find_line(code, ".call{value:")})
            recommendations.append("Use ReentrancyGuard from OpenZeppelin")
            
        # Check for tx.origin
        if "tx.origin" in code:
            issues.append({"severity": "high", "message": "Use of tx.origin for authentication", "line": find_line(code, "tx.origin")})
            recommendations.append("Use msg.sender instead of tx.origin")
            
        # Check for unchecked send/transfer
        if re.search(r"\.send\(|\.transfer\(", code):
            issues.append({"severity": "medium", "message": "Unchecked send/transfer", "line": find_line(code, ".send(")})
            recommendations.append("Check return values of low-level calls")
    
    elif language == "pyteal":
        if "Txn.sender()" in code:
            issues.append({"severity": "medium", "message": "Sender validation", "line": find_line(code, "Txn.sender()")})
            recommendations.append("Implement proper access control")
    
    elif language == "move":
        if "public fun" in code:
            issues.append({"severity": "low", "message": "Public function exposure", "line": find_line(code, "public fun")})
            recommendations.append("Consider function visibility")
    
    elif language == "rust":
        if "unsafe" in code:
            issues.append({"severity": "high", "message": "Unsafe code block", "line": find_line(code, "unsafe")})
            recommendations.append("Minimize use of unsafe blocks")
    
    # Calculate score based on issues
    score = calculate_score(issues)
    
    return {
        "score": score,
        "issues": issues,
        "recommendations": recommendations,
        "summary": f"Found {len(issues)} issues in {language} code"
    }

def find_line(code, pattern):
    lines = code.split('\n')
    for i, line in enumerate(lines, 1):
        if pattern in line:
            return i
    return 0

def calculate_score(issues):
    if not issues:
        return 100
        
    deductions = {
        "high": 20,
        "medium": 10,
        "low": 5
    }
    
    total_deduction = sum(deductions.get(issue["severity"], 0) for issue in issues)
    return max(0, 100 - total_deduction)
