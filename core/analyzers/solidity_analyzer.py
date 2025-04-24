from typing import Dict, Any, List
from .base_analyzer import BaseAnalyzer
import re

class SolidityAnalyzer(BaseAnalyzer):
    """Solidity smart contract analyzer for Ethereum"""
    
    @property
    def language(self) -> str:
        return "solidity"
        
    def analyze(self, code: str) -> Dict[str, Any]:
        """Analyze Solidity code"""
        issues = []
        
        # Check for common Solidity/Ethereum issues
        issues.extend(self.check_reentrancy(code))
        issues.extend(self.check_access_control(code))
        issues.extend(self.check_arithmetic(code))
        issues.extend(self.check_gas_optimization(code))
        issues.extend(self.check_security_patterns(code))
        
        # Calculate summary
        summary = self.generate_summary(issues)
        
        return {
            'issues': issues,
            'summary': summary
        }
        
    def check_reentrancy(self, code: str) -> List[Dict[str, Any]]:
        """Check for reentrancy vulnerabilities"""
        issues = []
        
        # Check for external calls before state changes
        external_calls = re.finditer(r'\.(?:call|send|transfer)\s*\(', code)
        for match in external_calls:
            # Look for state changes after the call
            state_changes = re.finditer(r'=\s*[^=]', code[match.end():])
            if next(state_changes, None):
                issues.append({
                    'severity': 'high',
                    'message': 'Potential reentrancy vulnerability: external call before state change',
                    'line': self.get_line_number(code, match.start()),
                    'type': 'reentrancy',
                    'category': 'Security'
                })
        
        return issues
        
    def check_access_control(self, code: str) -> List[Dict[str, Any]]:
        """Check for access control issues"""
        issues = []
        
        # Check for public functions without access control
        public_funcs = re.finditer(r'public\s+function\s+(\w+)', code)
        for match in public_funcs:
            func_name = match.group(1)
            if not self.has_access_control(func_name, code):
                issues.append({
                    'severity': 'high',
                    'message': f'Public function {func_name} lacks access control',
                    'line': self.get_line_number(code, match.start()),
                    'type': 'access-control',
                    'category': 'Security'
                })
        
        return issues
        
    def check_arithmetic(self, code: str) -> List[Dict[str, Any]]:
        """Check for arithmetic issues"""
        issues = []
        
        # Check for arithmetic operations without SafeMath
        if not re.search(r'using\s+SafeMath', code):
            arithmetic_ops = re.finditer(r'[+\-*/]\s*=', code)
            for match in arithmetic_ops:
                issues.append({
                    'severity': 'high',
                    'message': 'Arithmetic operation without SafeMath',
                    'line': self.get_line_number(code, match.start()),
                    'type': 'arithmetic',
                    'category': 'Security'
                })
        
        return issues
        
    def check_gas_optimization(self, code: str) -> List[Dict[str, Any]]:
        """Check for gas optimization issues"""
        issues = []
        
        # Check for unnecessary storage reads
        storage_reads = re.finditer(r'storage\s+\w+', code)
        for match in storage_reads:
            if not self.is_necessary_storage_read(match.group(0), code):
                issues.append({
                    'severity': 'medium',
                    'message': 'Unnecessary storage read',
                    'line': self.get_line_number(code, match.start()),
                    'type': 'gas-optimization',
                    'category': 'Performance'
                })
        
        # Check for loop optimizations
        loops = re.finditer(r'for\s*\(.*?\)', code)
        for match in loops:
            if not self.is_optimized_loop(match.group(0), code):
                issues.append({
                    'severity': 'medium',
                    'message': 'Loop may be optimized for gas',
                    'line': self.get_line_number(code, match.start()),
                    'type': 'gas-optimization',
                    'category': 'Performance'
                })
        
        return issues
        
    def check_security_patterns(self, code: str) -> List[Dict[str, Any]]:
        """Check for security patterns"""
        issues = []
        
        # Check for proper event emission
        if re.search(r'function\s+\w+.*?{', code) and not re.search(r'emit\s+\w+', code):
            issues.append({
                'severity': 'medium',
                'message': 'No events emitted for state changes',
                'type': 'best-practices',
                'category': 'Security'
            })
        
        # Check for proper error handling
        if not re.search(r'require\s*\(|revert\s*\(', code):
            issues.append({
                'severity': 'medium',
                'message': 'No error handling found',
                'type': 'error-handling',
                'category': 'Security'
            })
        
        return issues
        
    def has_access_control(self, func_name: str, code: str) -> bool:
        """Check if a function has access control"""
        func_body = re.search(rf'function\s+{func_name}.*?{{(.*?)}}', code, re.DOTALL)
        if func_body:
            return bool(re.search(r'require\s*\(.*?msg\.sender', func_body.group(1)))
        return False
        
    def is_necessary_storage_read(self, storage_var: str, code: str) -> bool:
        """Check if a storage read is necessary"""
        # This is a simplified check - in practice, you'd need more sophisticated analysis
        return bool(re.search(rf'{storage_var}\s*=', code))
        
    def is_optimized_loop(self, loop: str, code: str) -> bool:
        """Check if a loop is optimized"""
        # This is a simplified check - in practice, you'd need more sophisticated analysis
        return not bool(re.search(r'storage\s+\w+', loop))
        
    def get_line_number(self, code: str, pos: int) -> int:
        """Get line number for a position in code"""
        return code.count('\n', 0, pos) + 1
        
    def generate_summary(self, issues: List[Dict[str, Any]]) -> str:
        """Generate a summary of the analysis"""
        high_count = sum(1 for i in issues if i['severity'] == 'high')
        medium_count = sum(1 for i in issues if i['severity'] == 'medium')
        low_count = sum(1 for i in issues if i['severity'] == 'low')
        
        if high_count == 0 and medium_count == 0 and low_count == 0:
            return "No issues found. The contract appears to follow Solidity best practices."
        
        return f"Found {high_count} high severity, {medium_count} medium severity, and {low_count} low severity issues. Review recommended for production use."
        
    def get_severity_weights(self) -> Dict[str, int]:
        """Get Solidity-specific severity weights"""
        return {
            'high': 35,  # Higher weight for reentrancy and arithmetic issues
            'medium': 20,
            'low': 5
        }
        
    def get_platform_specific_rules(self) -> List[Dict[str, Any]]:
        """Get Solidity-specific analysis rules"""
        return [
            {
                'name': 'reentrancy',
                'description': 'Check for reentrancy vulnerabilities',
                'severity': 'high'
            },
            {
                'name': 'access-control',
                'description': 'Check for proper access control',
                'severity': 'high'
            },
            {
                'name': 'arithmetic',
                'description': 'Check for arithmetic safety',
                'severity': 'high'
            },
            {
                'name': 'gas-optimization',
                'description': 'Check for gas optimization issues',
                'severity': 'medium'
            }
        ] 