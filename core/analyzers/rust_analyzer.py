from typing import Dict, Any, List
from .base_analyzer import BaseAnalyzer
import re

class RustAnalyzer(BaseAnalyzer):
    """Rust smart contract analyzer for Solana/Polkadot"""
    
    @property
    def language(self) -> str:
        return "rust"
        
    def analyze(self, code: str) -> Dict[str, Any]:
        """Analyze Rust code"""
        issues = []
        
        # Check for common Rust smart contract issues
        issues.extend(self.check_memory_safety(code))
        issues.extend(self.check_error_handling(code))
        issues.extend(self.check_concurrency(code))
        issues.extend(self.check_gas_optimization(code))
        issues.extend(self.check_security_patterns(code))
        
        # Calculate summary
        summary = self.generate_summary(issues)
        
        return {
            'issues': issues,
            'summary': summary
        }
        
    def check_memory_safety(self, code: str) -> List[Dict[str, Any]]:
        """Check for memory safety issues"""
        issues = []
        
        # Check for unsafe blocks
        unsafe_blocks = re.finditer(r'unsafe\s*{', code)
        for match in unsafe_blocks:
            issues.append({
                'severity': 'high',
                'message': 'Unsafe block found in smart contract code',
                'line': self.get_line_number(code, match.start()),
                'type': 'memory-safety',
                'category': 'Security'
            })
        
        # Check for raw pointers
        raw_pointers = re.finditer(r'\*(?:const|mut)\s+\w+', code)
        for match in raw_pointers:
            issues.append({
                'severity': 'high',
                'message': 'Raw pointer usage found in smart contract code',
                'line': self.get_line_number(code, match.start()),
                'type': 'memory-safety',
                'category': 'Security'
            })
        
        return issues
        
    def check_error_handling(self, code: str) -> List[Dict[str, Any]]:
        """Check for error handling issues"""
        issues = []
        
        # Check for unwrap/expect usage
        unwrap_calls = re.finditer(r'\.(unwrap|expect)\s*\(', code)
        for match in unwrap_calls:
            issues.append({
                'severity': 'medium',
                'message': f'Use of {match.group(1)}() may panic',
                'line': self.get_line_number(code, match.start()),
                'type': 'error-handling',
                'category': 'Security'
            })
        
        # Check for proper error propagation
        if re.search(r'fn\s+\w+.*?->.*?Result', code, re.DOTALL):
            if not re.search(r'\?;', code):
                issues.append({
                    'severity': 'medium',
                    'message': 'Result-returning function without error propagation',
                    'type': 'error-handling',
                    'category': 'Best Practices'
                })
        
        return issues
        
    def check_concurrency(self, code: str) -> List[Dict[str, Any]]:
        """Check for concurrency issues"""
        issues = []
        
        # Check for proper mutex usage
        mutex_usage = re.finditer(r'Mutex\s*<', code)
        for match in mutex_usage:
            if not re.search(r'drop\s*\(', code[match.start():]):
                issues.append({
                    'severity': 'high',
                    'message': 'Mutex without explicit drop',
                    'line': self.get_line_number(code, match.start()),
                    'type': 'concurrency',
                    'category': 'Security'
                })
        
        # Check for proper atomic usage
        if re.search(r'Arc\s*<', code) and not re.search(r'atomic::', code):
            issues.append({
                'severity': 'medium',
                'message': 'Arc usage without atomic operations',
                'type': 'concurrency',
                'category': 'Security'
            })
        
        return issues
        
    def check_gas_optimization(self, code: str) -> List[Dict[str, Any]]:
        """Check for gas optimization issues"""
        issues = []
        
        # Check for clone in loops
        clone_in_loops = re.finditer(r'(?:for|while).*?{.*?\.clone\(\)', code, re.DOTALL)
        for match in clone_in_loops:
            issues.append({
                'severity': 'medium',
                'message': 'Clone operation in loop may be optimized',
                'line': self.get_line_number(code, match.start()),
                'type': 'gas-optimization',
                'category': 'Performance'
            })
        
        # Check for string allocations
        string_allocs = re.finditer(r'String::from|to_string\(\)', code)
        for match in string_allocs:
            issues.append({
                'severity': 'low',
                'message': 'String allocation may be optimized',
                'line': self.get_line_number(code, match.start()),
                'type': 'gas-optimization',
                'category': 'Performance'
            })
        
        return issues
        
    def check_security_patterns(self, code: str) -> List[Dict[str, Any]]:
        """Check for security patterns"""
        issues = []
        
        # Check for proper access control
        if re.search(r'pub\s+fn', code) and not re.search(r'require!|assert!', code):
            issues.append({
                'severity': 'high',
                'message': 'Public function without access control',
                'type': 'access-control',
                'category': 'Security'
            })
        
        # Check for proper validation
        if re.search(r'#\[instruction]', code) and not re.search(r'validate', code):
            issues.append({
                'severity': 'medium',
                'message': 'Instruction without validation',
                'type': 'input-validation',
                'category': 'Security'
            })
        
        # Platform-specific checks
        if '#[program]' in code:  # Solana
            if not re.search(r'Pubkey|AccountInfo', code):
                issues.append({
                    'severity': 'high',
                    'message': 'Solana program without proper account handling',
                    'type': 'platform-specific',
                    'category': 'Security'
                })
        elif '#[pallet]' in code:  # Substrate/Polkadot
            if not re.search(r'ensure!|weights::', code):
                issues.append({
                    'severity': 'high',
                    'message': 'Substrate pallet without proper weight handling',
                    'type': 'platform-specific',
                    'category': 'Security'
                })
        
        return issues
        
    def get_line_number(self, code: str, pos: int) -> int:
        """Get line number for a position in code"""
        return code.count('\n', 0, pos) + 1
        
    def generate_summary(self, issues: List[Dict[str, Any]]) -> str:
        """Generate a summary of the analysis"""
        high_count = sum(1 for i in issues if i['severity'] == 'high')
        medium_count = sum(1 for i in issues if i['severity'] == 'medium')
        low_count = sum(1 for i in issues if i['severity'] == 'low')
        
        if high_count == 0 and medium_count == 0 and low_count == 0:
            return "No issues found. The contract appears to follow Rust smart contract best practices."
        
        return f"Found {high_count} high severity, {medium_count} medium severity, and {low_count} low severity issues. Review recommended for production use."
        
    def get_severity_weights(self) -> Dict[str, int]:
        """Get Rust-specific severity weights"""
        return {
            'high': 35,  # Higher weight for memory safety issues
            'medium': 20,
            'low': 5
        }
        
    def get_platform_specific_rules(self) -> List[Dict[str, Any]]:
        """Get Rust-specific analysis rules"""
        return [
            {
                'name': 'memory-safety',
                'description': 'Check for memory safety issues',
                'severity': 'high'
            },
            {
                'name': 'error-handling',
                'description': 'Check for proper error handling',
                'severity': 'medium'
            },
            {
                'name': 'concurrency',
                'description': 'Check for concurrency issues',
                'severity': 'medium'
            },
            {
                'name': 'gas-optimization',
                'description': 'Check for gas optimization issues',
                'severity': 'low'
            }
        ] 