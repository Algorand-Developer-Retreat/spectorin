from typing import Dict, Any, List
from .base_analyzer import BaseAnalyzer
import re

class MoveAnalyzer(BaseAnalyzer):
    """Move smart contract analyzer for Aptos"""
    
    @property
    def language(self) -> str:
        return "move"
        
    def analyze(self, code: str) -> Dict[str, Any]:
        """Analyze Move code"""
        issues = []
        
        # Check for common Move/Aptos issues
        issues.extend(self.check_resource_safety(code))
        issues.extend(self.check_module_safety(code))
        issues.extend(self.check_formal_verification(code))
        issues.extend(self.check_gas_optimization(code))
        issues.extend(self.check_security_patterns(code))
        
        # Calculate summary
        summary = self.generate_summary(issues)
        
        return {
            'issues': issues,
            'summary': summary
        }
        
    def check_resource_safety(self, code: str) -> List[Dict[str, Any]]:
        """Check for resource safety issues"""
        issues = []
        
        # Check for resource drops
        resource_drops = re.finditer(r'let\s+(\w+)\s*:\s*(\w+)\s*=.*?(?!\buse\b|\bmove\b|\bcopy\b)', code)
        for match in resource_drops:
            var_name = match.group(1)
            type_name = match.group(2)
            if self.is_resource_type(type_name, code):
                issues.append({
                    'severity': 'high',
                    'message': f'Potential resource drop of {var_name}',
                    'line': self.get_line_number(code, match.start()),
                    'type': 'resource-safety',
                    'category': 'Security'
                })
        
        # Check for resource copies
        resource_copies = re.finditer(r'copy\s+(\w+)', code)
        for match in resource_copies:
            var_name = match.group(1)
            if self.is_resource_variable(var_name, code):
                issues.append({
                    'severity': 'high',
                    'message': f'Attempt to copy resource {var_name}',
                    'line': self.get_line_number(code, match.start()),
                    'type': 'resource-safety',
                    'category': 'Security'
                })
        
        return issues
        
    def check_module_safety(self, code: str) -> List[Dict[str, Any]]:
        """Check for module safety issues"""
        issues = []
        
        # Check for proper visibility modifiers
        public_funcs = re.finditer(r'public\s+fun\s+(\w+)', code)
        for match in public_funcs:
            func_name = match.group(1)
            if not self.has_abort_conditions(func_name, code):
                issues.append({
                    'severity': 'medium',
                    'message': f'Public function {func_name} lacks abort conditions',
                    'line': self.get_line_number(code, match.start()),
                    'type': 'module-safety',
                    'category': 'Security'
                })
        
        # Check for proper friend declarations
        if 'friend' in code and not re.search(r'use\s+0x1::signer', code):
            issues.append({
                'severity': 'medium',
                'message': 'Friend declaration without signer validation',
                'line': code.find('friend'),
                'type': 'module-safety',
                'category': 'Security'
            })
        
        return issues
        
    def check_formal_verification(self, code: str) -> List[Dict[str, Any]]:
        """Check for formal verification issues"""
        issues = []
        
        # Check for missing specifications
        public_funcs = re.finditer(r'public\s+fun\s+(\w+)', code)
        for match in public_funcs:
            func_name = match.group(1)
            if not self.has_spec(func_name, code):
                issues.append({
                    'severity': 'medium',
                    'message': f'Public function {func_name} lacks formal specification',
                    'line': self.get_line_number(code, match.start()),
                    'type': 'formal-verification',
                    'category': 'Best Practices'
                })
        
        # Check for missing invariants
        if re.search(r'struct\s+\w+', code) and not re.search(r'invariant', code):
            issues.append({
                'severity': 'low',
                'message': 'Struct defined without invariants',
                'type': 'formal-verification',
                'category': 'Best Practices'
            })
        
        return issues
        
    def check_gas_optimization(self, code: str) -> List[Dict[str, Any]]:
        """Check for gas optimization issues"""
        issues = []
        
        # Check for vector operations in loops
        vector_ops = re.finditer(r'while.*?\{.*?vector\[\d+\]', code, re.DOTALL)
        for match in vector_ops:
            issues.append({
                'severity': 'medium',
                'message': 'Vector operation in loop may be optimized',
                'line': self.get_line_number(code, match.start()),
                'type': 'gas-optimization',
                'category': 'Performance'
            })
        
        # Check for unnecessary copies
        copies = re.finditer(r'copy\s+(\w+).*?move\s+\1', code)
        for match in copies:
            issues.append({
                'severity': 'low',
                'message': 'Unnecessary copy before move',
                'line': self.get_line_number(code, match.start()),
                'type': 'gas-optimization',
                'category': 'Performance'
            })
        
        return issues
        
    def check_security_patterns(self, code: str) -> List[Dict[str, Any]]:
        """Check for security patterns"""
        issues = []
        
        # Check for signer validation
        if re.search(r'public\s+fun', code) and not re.search(r'signer::address_of', code):
            issues.append({
                'severity': 'high',
                'message': 'Public function without signer validation',
                'type': 'access-control',
                'category': 'Security'
            })
        
        # Check for proper error handling
        if not re.search(r'assert!\s*\(', code):
            issues.append({
                'severity': 'medium',
                'message': 'No assertions found in contract',
                'type': 'error-handling',
                'category': 'Security'
            })
        
        return issues
        
    def is_resource_type(self, type_name: str, code: str) -> bool:
        """Check if a type is a resource type"""
        return bool(re.search(rf'struct\s+{type_name}\s*{{\s*has\s+drop', code))
        
    def is_resource_variable(self, var_name: str, code: str) -> bool:
        """Check if a variable is of resource type"""
        var_decl = re.search(rf'let\s+{var_name}\s*:\s*(\w+)', code)
        if var_decl:
            return self.is_resource_type(var_decl.group(1), code)
        return False
        
    def has_abort_conditions(self, func_name: str, code: str) -> bool:
        """Check if a function has abort conditions"""
        func_body = re.search(rf'fun\s+{func_name}.*?{{(.*?)}}', code, re.DOTALL)
        if func_body:
            return bool(re.search(r'assert!|abort', func_body.group(1)))
        return False
        
    def has_spec(self, func_name: str, code: str) -> bool:
        """Check if a function has a specification"""
        return bool(re.search(rf'spec\s+{func_name}\s*{{', code))
        
    def get_line_number(self, code: str, pos: int) -> int:
        """Get line number for a position in code"""
        return code.count('\n', 0, pos) + 1
        
    def generate_summary(self, issues: List[Dict[str, Any]]) -> str:
        """Generate a summary of the analysis"""
        high_count = sum(1 for i in issues if i['severity'] == 'high')
        medium_count = sum(1 for i in issues if i['severity'] == 'medium')
        low_count = sum(1 for i in issues if i['severity'] == 'low')
        
        if high_count == 0 and medium_count == 0 and low_count == 0:
            return "No issues found. The contract appears to follow Move/Aptos best practices."
        
        return f"Found {high_count} high severity, {medium_count} medium severity, and {low_count} low severity issues. Review recommended for production use."
        
    def get_severity_weights(self) -> Dict[str, int]:
        """Get Move-specific severity weights"""
        return {
            'high': 40,  # Higher weight for resource safety issues
            'medium': 20,
            'low': 5
        }
        
    def get_platform_specific_rules(self) -> List[Dict[str, Any]]:
        """Get Move-specific analysis rules"""
        return [
            {
                'name': 'resource-safety',
                'description': 'Check for proper resource handling',
                'severity': 'high'
            },
            {
                'name': 'module-safety',
                'description': 'Check for proper module safety',
                'severity': 'medium'
            },
            {
                'name': 'formal-verification',
                'description': 'Check for formal verification',
                'severity': 'medium'
            },
            {
                'name': 'gas-optimization',
                'description': 'Check for gas optimization issues',
                'severity': 'low'
            }
        ] 