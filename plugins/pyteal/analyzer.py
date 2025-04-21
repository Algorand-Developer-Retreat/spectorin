from core.z3.smart_contract_adapter import SmartContractToZ3Adapter
import os
import re

class Analyzer:
    def __init__(self):
        self.adapter = SmartContractToZ3Adapter()
    
    def analyze(self, path: str):
        """
        Analyze PyTeal smart contracts for security issues
        """
        issues = []
        recommendations = []
        
        if os.path.isfile(path):
            try:
                with open(path, 'r') as f:
                    code = f.read()
                
                # Perform basic security checks
                self._check_security_patterns(code, issues)
                
                # Build recommendations based on issues
                recommendations = self._generate_recommendations(issues)
                
                # Calculate security score
                score = self._calculate_security_score(issues)
                
                return {
                    "issues": issues,
                    "recommendations": recommendations,
                    "score": score,
                    "summary": f"PyTeal Analysis complete. Security Score: {score}/100"
                }
                
            except Exception as e:
                return {
                    "issues": [{"severity": "error", "message": f"Analysis error: {str(e)}"}],
                    "score": 0,
                    "summary": "Analysis failed due to errors"
                }
        else:
            # Directory handling
            return {
                "issues": [{"severity": "info", "message": "Directory scanning not implemented yet"}],
                "score": 50,
                "summary": "Directory analysis not fully implemented"
            }
    
    def _check_security_patterns(self, code, issues):
        """
        Check for common PyTeal security issues using regex patterns
        """
        # Check for unchecked inputs
        if not re.search(r'Assert\(', code):
            issues.append({
                "severity": "high",
                "message": "No input validation using Assert() found",
                "line": None
            })
        
        # Check for potential overflows
        if re.search(r'\+|\*', code) and not re.search(r'Assert\(.*<|Assert\(.*>', code):
            issues.append({
                "severity": "medium",
                "message": "Arithmetic operations without bounds checking",
                "line": self._find_line_number(code, r'\+|\*')
            })
        
        # Check for potential unauthorized operations
        if re.search(r'Balance\(|Transfer\(', code) and not re.search(r'Txn\.sender', code):
            issues.append({
                "severity": "high",
                "message": "Balance or Transfer operations without sender verification",
                "line": self._find_line_number(code, r'Balance\(|Transfer\(')
            })
    
    def _find_line_number(self, code, pattern):
        """Helper to find the line number for a regex match"""
        lines = code.split('\n')
        for i, line in enumerate(lines):
            if re.search(pattern, line):
                return i + 1
        return None
            
    def _calculate_security_score(self, issues):
        """
        Calculate a security score based on the number and severity of issues
        """
        if not issues:
            return 100
            
        score = 100
        for issue in issues:
            if issue["severity"] == "high":
                score -= 20
            elif issue["severity"] == "medium":
                score -= 10
            elif issue["severity"] == "low": 
                score -= 5
                
        return max(0, score)
    
    def _generate_recommendations(self, issues):
        """Generate recommendations based on issues found"""
        recommendations = []
        
        for issue in issues:
            if "Assert" in issue["message"]:
                recommendations.append("Add Assert() statements to validate inputs and state transitions")
            
            if "arithmetic operations" in issue["message"]:
                recommendations.append("Add bounds checking for all arithmetic operations")
            
            if "sender verification" in issue["message"]:
                recommendations.append("Verify Txn.sender before performing sensitive operations")
        
        # Add general recommendations
        recommendations.append("Consider using the Application Call Transaction Fields to validate application calls")
        recommendations.append("Implement atomic transfers for operations requiring atomicity")
        
        return recommendations 