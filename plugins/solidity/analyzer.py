from core.analyzers.base_analyzer import BaseAnalyzer
from typing import Dict, Any, List
import re

class SolidityAnalyzer(BaseAnalyzer):
    @property
    def language(self) -> str:
        return "solidity"
    
    def analyze(self, code: str) -> Dict[str, Any]:
        issues: List[Dict[str, Any]] = []
        
        # Check for reentrancy vulnerabilities
        if re.search(r'\.call{.*value.*}', code):
            issues.append({
                'severity': 'high',
                'message': 'Potential reentrancy vulnerability detected',
                'line': self._find_line_number(code, r'\.call{.*value.*}')
            })
            
        # Check for unchecked return values
        if re.search(r'\.send\(|\.transfer\(', code):
            issues.append({
                'severity': 'medium',
                'message': 'Use of send/transfer without checking return value',
                'line': self._find_line_number(code, r'\.send\(|\.transfer\(')
            })
            
        return {
            'issues': issues,
            'summary': f'Found {len(issues)} potential issues'
        }
        
    def _find_line_number(self, code: str, pattern: str) -> int:
        lines = code.split('\n')
        for i, line in enumerate(lines, 1):
            if re.search(pattern, line):
                return i
        return 0
