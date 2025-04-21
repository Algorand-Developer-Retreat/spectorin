from abc import ABC, abstractmethod
from typing import Dict, Any, List
import pluggy

hookimpl = pluggy.HookimplMarker("spectorin")

class BaseAnalyzer(ABC):
    """Base class for all language-specific analyzers"""
    
    @hookimpl
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
        """Calculate security score from analysis results"""
        # Default implementation
        issues = analysis_results.get('issues', [])
        if not issues:
            return 100
            
        # Calculate score based on issue severity
        severity_weights = {
            'high': 30,
            'medium': 15,
            'low': 5
        }
        
        total_deduction = sum(
            severity_weights.get(issue['severity'], 0)
            for issue in issues
        )
        
        return max(0, 100 - total_deduction) 