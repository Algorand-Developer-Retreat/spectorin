import os
import re

class Analyzer:
    def analyze(self, path: str):
        """
        Analyze Rust smart contracts for security issues
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
                    "summary": f"Rust Analysis complete. Security Score: {score}/100"
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
        Check for common Rust smart contract security issues using regex patterns
        """
        # Check for unsafe blocks
        unsafe_matches = re.finditer(r'unsafe\s*{', code)
        for match in unsafe_matches:
            issues.append({
                "severity": "high",
                "message": "Unsafe block detected - could lead to memory safety issues",
                "line": code[:match.start()].count('\n') + 1
            })
        
        # Check for proper error handling
        if re.search(r'fn\s+\w+', code) and not re.search(r'Result<', code):
            issues.append({
                "severity": "medium", 
                "message": "Functions without Result return type - potential lack of error handling",
                "line": None
            })
        
        # Check for unvalidated inputs
        if re.search(r'pub\s+fn', code) and not re.search(r'assert', code):
            issues.append({
                "severity": "medium",
                "message": "Public functions without input validation",
                "line": self._find_line_number(code, r'pub\s+fn')
            })
            
        # Check for reentrancy protection in cross-contract calls
        if re.search(r'AccountId|account_id|cross_contract', code, re.IGNORECASE) and not re.search(r'ReentrancyGuard|mutex|lock', code, re.IGNORECASE):
            issues.append({
                "severity": "high",
                "message": "Potential reentrancy vulnerability in cross-contract calls",
                "line": None
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
            if "Unsafe block" in issue["message"]:
                recommendations.append("Remove unsafe blocks or ensure they're properly reviewed for security issues")
            
            if "Result return type" in issue["message"]:
                recommendations.append("Use Result<T, E> return type for functions that can fail")
            
            if "input validation" in issue["message"]:
                recommendations.append("Add input validation with assertions or custom validation logic")
            
            if "reentrancy" in issue["message"]:
                recommendations.append("Implement reentrancy guards or mutex patterns for cross-contract calls")
        
        # Add general recommendations
        recommendations.append("Use typestates to enforce correct API usage at compile time")
        recommendations.append("Consider formal verification using tools like KLEE or Crux")
        
        return recommendations 