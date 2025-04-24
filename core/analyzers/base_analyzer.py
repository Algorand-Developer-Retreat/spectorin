from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
import pluggy
import logging
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)

class Severity(Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"

@dataclass
class SecurityIssue:
    title: str
    description: str
    severity: Severity
    line: Optional[int] = None
    column: Optional[int] = None
    code_snippet: Optional[str] = None
    recommendation: Optional[str] = None
    cwe_id: Optional[str] = None
    references: Optional[List[str]] = None

hookspec = pluggy.HookspecMarker("spectorin")
hookimpl = pluggy.HookimplMarker("spectorin")

class BaseAnalyzer(ABC):
    """Base class for all language-specific analyzers"""
    
    def __init__(self):
        self.issues: List[SecurityIssue] = []
        self.metrics: Dict[str, Any] = {}
    
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
        deductions = {severity.value: 0 for severity in Severity}
        
        # Count issues by severity
        issue_counts = {severity.value: 0 for severity in Severity}
        
        for issue in issues:
            severity = issue.get('severity', Severity.LOW.value)
            issue_counts[severity] += 1
            
            # Calculate deduction based on severity weight
            weight = severity_weights.get(severity, 0)
            
            # Apply diminishing returns for multiple issues of same severity
            deduction = weight * (1 / (1 + issue_counts[severity] * 0.3))
            
            # Additional penalty for critical issues
            if severity == Severity.CRITICAL.value:
                deduction *= 1.5
                
            deductions[severity] += deduction
        
        # Calculate final score with diminishing returns
        total_deduction = sum(deductions.values())
        
        # Apply a more gradual deduction curve
        final_score = base_score - (total_deduction * 0.7)
        
        # Ensure minimum score based on contract structure
        if issue_counts[Severity.CRITICAL.value] < 5:  # If not completely broken
            final_score = max(20, final_score)
        
        # Ensure score is between 0 and 100
        return max(0, min(100, int(final_score)))
    
    def get_severity_weights(self) -> Dict[str, int]:
        """Get platform-specific severity weights"""
        return {
            Severity.CRITICAL.value: 15,
            Severity.HIGH.value: 10,
            Severity.MEDIUM.value: 5,
            Severity.LOW.value: 2,
            Severity.INFO.value: 0
        }
    
    def get_platform_specific_rules(self) -> List[Dict[str, Any]]:
        """Get platform-specific analysis rules"""
        return []
    
    def validate_platform_specific_patterns(self, code: str) -> List[SecurityIssue]:
        """Validate platform-specific patterns and best practices"""
        return []
    
    def check_platform_specific_vulnerabilities(self, code: str) -> List[SecurityIssue]:
        """Check for platform-specific vulnerabilities"""
        return []
    
    def add_issue(self, issue: SecurityIssue):
        """Add a security issue to the analysis results"""
        self.issues.append(issue)
        logger.info(f"Found {issue.severity.value} severity issue: {issue.title}")
    
    def get_analysis_summary(self) -> Dict[str, Any]:
        """Get a summary of the analysis results"""
        return {
            'total_issues': len(self.issues),
            'issues_by_severity': {
                severity.value: len([i for i in self.issues if i.severity == severity])
                for severity in Severity
            },
            'metrics': self.metrics
        }
    
    def check_common_vulnerabilities(self, code: str) -> List[SecurityIssue]:
        """Check for common vulnerabilities across all platforms"""
        issues = []
        
        # Check for hardcoded secrets
        if any(secret in code.lower() for secret in ['private_key', 'secret_key', 'api_key']):
            issues.append(SecurityIssue(
                title="Hardcoded Secret",
                description="Found potential hardcoded secret in the code",
                severity=Severity.HIGH,
                recommendation="Move secrets to environment variables or secure storage"
            ))
        
        # Check for unsafe math operations
        if any(op in code for op in ['+', '-', '*', '/']):
            issues.append(SecurityIssue(
                title="Unsafe Math Operation",
                description="Found potential unsafe math operation",
                severity=Severity.MEDIUM,
                recommendation="Use safe math libraries for arithmetic operations"
            ))
        
        return issues
    
    def analyze_dependencies(self, dependencies: List[str]) -> List[SecurityIssue]:
        """Analyze dependencies for known vulnerabilities"""
        issues = []
        # Implement dependency analysis logic here
        return issues
    
    def check_code_quality(self, code: str) -> List[SecurityIssue]:
        """Check code quality and best practices"""
        issues = []
        # Implement code quality checks here
        return issues 