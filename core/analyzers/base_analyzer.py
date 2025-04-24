from abc import ABC, abstractmethod
from typing import Dict, Any, List
import pluggy

hookspec = pluggy.HookspecMarker("spectorin")
hookimpl = pluggy.HookimplMarker("spectorin")

class BaseAnalyzer(ABC):
    """Base class for all language-specific analyzers"""
    
    @hookspec
    def get_analyzer(self, language: str):
        """Return self if language matches"""
        if language.lower() == self.language:
            return self
        return None
    
    @property
    @abstractmethod
    def language(self) -> str:
        """Language identifier"""
        pass
    
    @abstractmethod
    def analyze(self, code: str) -> Dict[str, Any]:
        """Analyze code and return results"""
        pass
    
    def calculate_security_score(self, analysis_results: Dict[str, Any]) -> int:
        """Calculate security score from analysis results with platform-specific weights"""
        issues = analysis_results.get('issues', [])
        if not issues:
            return 100
            
        # Platform-specific severity weights
        severity_weights = self.get_severity_weights()
        
        # Initialize score components
        base_score = 100
        deductions = {
            'high': 0,
            'medium': 0,
            'low': 0
        }
        
        # Count issues by severity
        issue_counts = {
            'high': 0,
            'medium': 0,
            'low': 0
        }
        
        for issue in issues:
            severity = issue.get('severity', 'low')
            issue_counts[severity] += 1
            
            # Calculate deduction based on severity weight
            weight = severity_weights.get(severity, 0)
            
            # Apply diminishing returns for multiple issues of same severity
            # This prevents the score from dropping too quickly
            deduction = weight * (1 / (1 + issue_counts[severity] * 0.3))
            
            # Additional penalty for critical issues
            if issue.get('critical', False):
                deduction *= 1.2  # Reduced from 1.5
                
            deductions[severity] += deduction
        
        # Calculate final score with diminishing returns
        total_deduction = sum(deductions.values())
        
        # Apply a more gradual deduction curve
        final_score = base_score - (total_deduction * 0.7)  # Reduced impact of deductions
        
        # Ensure minimum score based on contract structure
        # If the contract has basic structure (not just syntax errors),
        # give it at least a 20% score
        if issue_counts['high'] < 10:  # If not completely broken
            final_score = max(20, final_score)
        
        # Ensure score is between 0 and 100
        return max(0, min(100, int(final_score)))
    
    def get_severity_weights(self) -> Dict[str, int]:
        """Get platform-specific severity weights"""
        return {
            'high': 8,     # Further reduced to be less punitive
            'medium': 4,   # Further reduced
            'low': 2       # Further reduced
        }
    
    def get_platform_specific_rules(self) -> List[Dict[str, Any]]:
        """Get platform-specific analysis rules"""
        return []
    
    def validate_platform_specific_patterns(self, code: str) -> List[Dict[str, Any]]:
        """Validate platform-specific patterns and best practices"""
        return []
    
    def check_platform_specific_vulnerabilities(self, code: str) -> List[Dict[str, Any]]:
        """Check for platform-specific vulnerabilities"""
        return [] 