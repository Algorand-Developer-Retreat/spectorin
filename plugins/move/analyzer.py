import os
import re

class Analyzer:
    def analyze(self, path: str):
        """
        Analyze Move smart contracts for security issues
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
                    "summary": f"Move Analysis complete. Security Score: {score}/100"
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
        Check for common Move security issues using regex patterns
        """
        # Check for unrestricted access to sensitive functions
        if re.search(r'public\s+fun\s+transfer', code, re.IGNORECASE):
            if not re.search(r'assert!\(', code, re.IGNORECASE):
                issues.append({
                    "severity": "high",
                    "message": "Public transfer function without assertions for access control",
                    "line": self._find_line_number(code, r'public\s+fun\s+transfer')
                })
        
        # Check for proper error handling
        if not re.search(r'abort', code, re.IGNORECASE):
            issues.append({
                "severity": "medium",
                "message": "No abort statements found - potential lack of error handling",
                "line": None
            })
        
        # Check for resource safety
        if re.search(r'drop', code, re.IGNORECASE) and not re.search(r'key', code, re.IGNORECASE):
            issues.append({
                "severity": "medium",
                "message": "Resource may be dropped without proper cleanup",
                "line": self._find_line_number(code, r'drop')
            })
    
    def _find_line_number(self, code, pattern):
        """Helper to find the line number for a regex match"""
        lines = code.split('\n')
        for i, line in enumerate(lines):
            if re.search(pattern, line, re.IGNORECASE):
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
            if "access control" in issue["message"]:
                recommendations.append("Add access control checks using assert! to restrict access to transfer functions")
            
            if "error handling" in issue["message"]:
                recommendations.append("Add proper error handling with abort statements in critical functions")
            
            if "Resource" in issue["message"]:
                recommendations.append("Ensure resources are properly managed and can't be lost")
        
        # Add general recommendations
        recommendations.append("Use the Move Prover to formally verify critical properties")
        recommendations.append("Consider using a well-tested access control pattern for authorization")
        
        return recommendations 