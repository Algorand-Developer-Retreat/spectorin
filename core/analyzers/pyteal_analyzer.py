from typing import Dict, Any, List
from .base_analyzer import BaseAnalyzer, hookimpl
import ast
import re

class PyTealAnalyzer(BaseAnalyzer):
    """PyTeal smart contract analyzer"""
    
    @property
    @hookimpl
    def language(self) -> str:
        return "pyteal"
        
    @hookimpl
    def analyze(self, code: str) -> Dict[str, Any]:
        """Analyze PyTeal code"""
        issues = []
        
        # Parse Python AST
        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            issues.append({
                'severity': 'high',
                'message': f'Syntax error: {str(e)}',
                'line': getattr(e, 'lineno', 0),
                'type': 'syntax',
                'category': 'Code Quality'
            })
            return {'issues': issues}
            
        # Check for common PyTeal/Algorand issues
        issues.extend(self.check_atomic_transfers(tree))
        issues.extend(self.check_input_validation(tree))
        issues.extend(self.check_state_management(tree))
        issues.extend(self.check_gas_optimization(tree))
        issues.extend(self.check_security_patterns(tree))
        
        # Calculate summary
        summary = self.generate_summary(issues)
        
        # Create analysis results
        analysis_results = {
            'issues': issues,
            'summary': summary
        }
        
        # Calculate security score
        score = self.calculate_security_score(analysis_results)
        analysis_results['score'] = score
        
        return analysis_results
        
    def check_atomic_transfers(self, tree: ast.AST) -> List[Dict[str, Any]]:
        """Check for proper atomic transfer usage"""
        issues = []
        
        # Look for multiple payment operations without atomic transfer
        payment_ops = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                if hasattr(node, 'func') and isinstance(node.func, ast.Name):
                    if node.func.id in ['PaymentTxn', 'AssetTransferTxn']:
                        payment_ops.append(node)
        
        if len(payment_ops) > 1:
            atomic_found = False
            for node in ast.walk(tree):
                if isinstance(node, ast.Call):
                    if hasattr(node, 'func') and isinstance(node.func, ast.Name):
                        if node.func.id in ['AtomicTransfer', 'Group']:
                            atomic_found = True
                            break
            
            if not atomic_found:
                issues.append({
                    'severity': 'high',
                    'message': 'Multiple payment operations found without atomic transfer',
                    'line': payment_ops[0].lineno,
                    'type': 'atomic',
                    'category': 'Security'
                })
        
        # Check for proper group transaction validation
        group_txn_found = False
        group_size_check_found = False
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                if hasattr(node, 'func') and isinstance(node.func, ast.Name):
                    if node.func.id in ['Group', 'AtomicTransfer']:
                        group_txn_found = True
                        # Look for group size validation
                        parent = self.find_parent_stmt(tree, node)
                        if parent:
                            for sibling in ast.walk(parent):
                                if isinstance(sibling, ast.Call):
                                    if hasattr(sibling, 'func') and isinstance(sibling.func, ast.Name):
                                        if sibling.func.id == 'Global.group_size':
                                            group_size_check_found = True
                                            break
        
        if group_txn_found and not group_size_check_found:
            issues.append({
                'severity': 'medium',
                'message': 'Group transaction found without proper group size validation',
                'line': 0,
                'type': 'group-validation',
                'category': 'Security'
            })
        
        return issues
        
    def check_input_validation(self, tree: ast.AST) -> List[Dict[str, Any]]:
        """Check for proper input validation"""
        issues = []
        
        for node in ast.walk(tree):
            # Check for application args access without validation
            if isinstance(node, ast.Subscript):
                if isinstance(node.value, ast.Attribute):
                    if hasattr(node.value, 'attr') and node.value.attr == 'application_args':
                        validation_found = False
                        parent = self.find_parent_stmt(tree, node)
                        if parent:
                            for sibling in ast.walk(parent):
                                if isinstance(sibling, ast.Call):
                                    if hasattr(sibling, 'func') and isinstance(sibling.func, ast.Name):
                                        if sibling.func.id in ['Assert', 'Reject']:
                                            validation_found = True
                                            break
                        
                        if not validation_found:
                            issues.append({
                                'severity': 'high',
                                'message': 'Application argument used without validation',
                                'line': getattr(node, 'lineno', 0),
                                'type': 'input-validation',
                                'category': 'Security'
                            })
            
            # Check for account index access without validation
            if isinstance(node, ast.Subscript):
                if isinstance(node.value, ast.Attribute):
                    if hasattr(node.value, 'attr') and node.value.attr == 'accounts':
                        validation_found = False
                        parent = self.find_parent_stmt(tree, node)
                        if parent:
                            for sibling in ast.walk(parent):
                                if isinstance(sibling, ast.Call):
                                    if hasattr(sibling, 'func') and isinstance(sibling.func, ast.Name):
                                        if sibling.func.id in ['Assert', 'Global.group_size']:
                                            validation_found = True
                                            break
                        
                        if not validation_found:
                            issues.append({
                                'severity': 'high',
                                'message': 'Account index used without validation',
                                'line': getattr(node, 'lineno', 0),
                                'type': 'input-validation',
                                'category': 'Security'
                            })
            
            # Check for numeric input validation
            if isinstance(node, ast.Call):
                if hasattr(node, 'func') and isinstance(node.func, ast.Name):
                    if node.func.id == 'Btoi':
                        validation_found = False
                        parent = self.find_parent_stmt(tree, node)
                        if parent:
                            for sibling in ast.walk(parent):
                                if isinstance(sibling, ast.Call):
                                    if hasattr(sibling, 'func') and isinstance(sibling.func, ast.Name):
                                        if sibling.func.id in ['Assert', 'Reject']:
                                            validation_found = True
                                            break
                        
                        if not validation_found:
                            issues.append({
                                'severity': 'high',
                                'message': 'Numeric conversion without bounds checking',
                                'line': getattr(node, 'lineno', 0),
                                'type': 'input-validation',
                                'category': 'Security'
                            })
        
        return issues
        
    def check_state_management(self, tree: ast.AST) -> List[Dict[str, Any]]:
        """Check for proper state management"""
        issues = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Attribute):
                    # Check for global state modifications without checks
                    if node.func.attr == 'globalPut':
                        check_found = False
                        parent = self.find_parent_stmt(tree, node)
                        if parent:
                            for sibling in ast.walk(parent):
                                if isinstance(sibling, ast.Call):
                                    if hasattr(sibling, 'func') and isinstance(sibling.func, ast.Name):
                                        if sibling.func.id in ['Assert', 'App.globalGet']:
                                            check_found = True
                                            break
                        
                        if not check_found:
                            issues.append({
                                'severity': 'medium',
                                'message': 'Global state modification without proper checks',
                                'line': getattr(node, 'lineno', 0),
                                'type': 'state-management',
                                'category': 'Security'
                            })
                    
                    # Check for box storage usage
                    if node.func.attr.startswith('box_'):
                        size_check_found = False
                        parent = self.find_parent_stmt(tree, node)
                        if parent:
                            for sibling in ast.walk(parent):
                                if isinstance(sibling, ast.Call):
                                    if hasattr(sibling, 'func') and isinstance(sibling.func, ast.Name):
                                        if sibling.func.id in ['Assert', 'Reject']:
                                            size_check_found = True
                                            break
                        
                        if not size_check_found:
                            issues.append({
                                'severity': 'medium',
                                'message': 'Box storage operation without size validation',
                                'line': getattr(node, 'lineno', 0),
                                'type': 'state-management',
                                'category': 'Resource Management'
                            })
        
        return issues
        
    def check_gas_optimization(self, tree: ast.AST) -> List[Dict[str, Any]]:
        """Check for gas optimization issues"""
        issues = []
        
        # Check for unnecessary operations in loops
        for node in ast.walk(tree):
            if isinstance(node, (ast.For, ast.While)):
                for op in ast.walk(node):
                    if isinstance(op, ast.Call):
                        if hasattr(op, 'func') and isinstance(op.func, ast.Name):
                            if op.func.id in ['App.globalGet', 'App.localGet']:
                                issues.append({
                                    'severity': 'medium',
                                    'message': 'State access in loop may be optimized',
                                    'line': op.lineno,
                                    'type': 'gas-optimization',
                                    'category': 'Performance'
                                })
        
        # Check for unnecessary state reads
        state_reads = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                if hasattr(node, 'func') and isinstance(node.func, ast.Name):
                    if node.func.id in ['App.globalGet', 'App.localGet']:
                        state_reads.append(node)
        
        # Check if the same state is read multiple times
        for i, read1 in enumerate(state_reads):
            for read2 in state_reads[i+1:]:
                if self.is_same_state_read(read1, read2):
                    issues.append({
                        'severity': 'low',
                        'message': 'Same state read multiple times - consider caching',
                        'line': read1.lineno,
                        'type': 'gas-optimization',
                        'category': 'Performance'
                    })
        
        return issues
        
    def check_security_patterns(self, tree: ast.AST) -> List[Dict[str, Any]]:
        """Check for security patterns"""
        issues = []
        
        # Check for proper creator checks
        creator_check_found = False
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Attribute):
                    if node.func.attr == 'Execute':
                        # Check for inner transaction error handling
                        error_handling_found = False
                        parent = self.find_parent_stmt(tree, node)
                        if parent:
                            for sibling in ast.walk(parent):
                                if isinstance(sibling, ast.Call):
                                    if hasattr(sibling, 'func') and isinstance(sibling.func, ast.Name):
                                        if sibling.func.id in ['Try', 'Assert']:
                                            error_handling_found = True
                                            break
                        
                        if not error_handling_found:
                            issues.append({
                                'severity': 'high',
                                'message': 'Inner transaction without proper error handling',
                                'line': getattr(node, 'lineno', 0),
                                'type': 'error-handling',
                                'category': 'Security'
                            })
            
            # Check for creator check
            if isinstance(node, ast.Compare):
                if isinstance(node.left, ast.Attribute):
                    if node.left.attr == 'sender' and any(isinstance(comp, ast.Eq) for comp in node.ops):
                        for comparator in node.comparators:
                            if isinstance(comparator, ast.Call):
                                if isinstance(comparator.func, ast.Attribute):
                                    if comparator.func.attr == 'creator_address':
                                        creator_check_found = True
                                        break
        
        if not creator_check_found:
            issues.append({
                'severity': 'medium',
                'message': 'No creator check found in contract',
                'line': 0,
                'type': 'access-control',
                'category': 'Security'
            })
        
        # Check for proper asset clawback handling
        clawback_found = False
        clawback_validation_found = False
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                if hasattr(node, 'func') and isinstance(node.func, ast.Name):
                    if node.func.id == 'AssetTransfer' and hasattr(node, 'attr') and node.attr == 'clawback_addr':
                        clawback_found = True
                        # Look for validation
                        parent = self.find_parent_stmt(tree, node)
                        if parent:
                            for sibling in ast.walk(parent):
                                if isinstance(sibling, ast.Call):
                                    if hasattr(sibling, 'func') and isinstance(sibling.func, ast.Name):
                                        if sibling.func.id in ['Assert', 'Reject']:
                                            clawback_validation_found = True
                                            break
        
        if clawback_found and not clawback_validation_found:
            issues.append({
                'severity': 'high',
                'message': 'Asset clawback operation without proper validation',
                'line': 0,
                'type': 'asset-security',
                'category': 'Security'
            })
        
        return issues
        
    def is_same_state_read(self, read1: ast.Call, read2: ast.Call) -> bool:
        """Check if two state reads are accessing the same state"""
        if not (hasattr(read1, 'func') and hasattr(read2, 'func')):
            return False
            
        if read1.func.id != read2.func.id:
            return False
            
        # Check if they're accessing the same key
        if len(read1.args) != len(read2.args):
            return False
            
        for arg1, arg2 in zip(read1.args, read2.args):
            if isinstance(arg1, ast.Constant) and isinstance(arg2, ast.Constant):
                if arg1.value != arg2.value:
                    return False
            elif isinstance(arg1, ast.Name) and isinstance(arg2, ast.Name):
                if arg1.id != arg2.id:
                    return False
            else:
                return False
                
        return True
        
    def find_parent_stmt(self, tree: ast.AST, target_node: ast.AST) -> ast.AST:
        """Find the parent statement of a node"""
        for node in ast.walk(tree):
            for child in ast.iter_child_nodes(node):
                if child == target_node:
                    return node
        return None
        
    def generate_summary(self, issues: List[Dict[str, Any]]) -> str:
        """Generate a summary of the analysis"""
        high_count = sum(1 for i in issues if i['severity'] == 'high')
        medium_count = sum(1 for i in issues if i['severity'] == 'medium')
        low_count = sum(1 for i in issues if i['severity'] == 'low')
        
        if high_count == 0 and medium_count == 0 and low_count == 0:
            return "No issues found. The contract appears to follow Algorand best practices."
        
        return f"Found {high_count} high severity, {medium_count} medium severity, and {low_count} low severity issues. Review recommended for production use."
        
    @hookimpl
    def get_severity_weights(self) -> Dict[str, int]:
        """Get PyTeal-specific severity weights"""
        return {
            'high': 35,  # Higher weight for atomic transfer issues
            'medium': 20,
            'low': 5
        }
        
    @hookimpl
    def get_platform_specific_rules(self) -> List[Dict[str, Any]]:
        """Get PyTeal-specific analysis rules"""
        return [
            {
                'name': 'atomic-transfers',
                'description': 'Check for proper atomic transfer usage',
                'severity': 'high'
            },
            {
                'name': 'input-validation',
                'description': 'Check for proper input validation',
                'severity': 'medium'
            },
            {
                'name': 'state-management',
                'description': 'Check for proper state management',
                'severity': 'medium'
            },
            {
                'name': 'gas-optimization',
                'description': 'Check for gas optimization issues',
                'severity': 'low'
            }
        ]
        
    @hookimpl
    def validate_platform_specific_patterns(self, code: str) -> List[Dict[str, Any]]:
        """Validate PyTeal-specific patterns and best practices"""
        issues = []
        
        # Check for recommended PyTeal patterns
        patterns = [
            (r'\.application_args\[\d+\]', 'Consider using named constants for application args indices'),
            (r'Int\(1\)\s*==\s*Int\(1\)', 'Unnecessary comparison of identical values'),
            (r'Txn\.sender\s*==\s*Global\.creator_address\(\)', 'Consider extracting creator check into a reusable function'),
            (r'Seq\(\[.*?\]\)', 'Consider using Seq without list for better readability'),
            (r'If\(.*?,\s*Return\(.*?\),\s*Return\(.*?\)\)', 'Consider using Cond for multiple conditions')
        ]
        
        for pattern, message in patterns:
            matches = re.finditer(pattern, code)
            for match in matches:
                line_number = code[:match.start()].count('\n') + 1
                issues.append({
                    'severity': 'low',
                    'message': message,
                    'line': line_number,
                    'type': 'pattern',
                    'category': 'Best Practice'
                })
        
        return issues
    
    @hookimpl
    def check_platform_specific_vulnerabilities(self, code: str) -> List[Dict[str, Any]]:
        """Check for PyTeal-specific vulnerabilities"""
        issues = []
        
        # Check for common PyTeal vulnerabilities
        vulnerabilities = [
            (r'AssetTransfer\.clawback_addr', {
                'severity': 'high',
                'message': 'Clawback address usage detected - ensure this is intentional',
                'type': 'security',
                'category': 'Asset Security'
            }),
            (r'App\.box_\w+\s*\([^)]*\)', {
                'severity': 'medium',
                'message': 'Box storage usage detected - verify size limits and cost considerations',
                'type': 'resource',
                'category': 'Resource Management'
            }),
            (r'InnerTxnBuilder\.Execute\(\)', {
                'severity': 'medium',
                'message': 'Inner transaction detected - verify proper error handling and effects',
                'type': 'security',
                'category': 'Transaction Security'
            }),
            (r'Global\.group_size\(\)', {
                'severity': 'medium',
                'message': 'Group size check detected - ensure proper validation of group transaction',
                'type': 'security',
                'category': 'Transaction Security'
            })
        ]
        
        for pattern, issue_info in vulnerabilities:
            matches = re.finditer(pattern, code)
            for match in matches:
                line_number = code[:match.start()].count('\n') + 1
                issue = issue_info.copy()
                issue['line'] = line_number
                issues.append(issue)
        
        return issues 