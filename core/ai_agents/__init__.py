class AIAgent:
    """
    AI Agent for generating recommendations, properties, and specs
    """
    
    def generate_recommendations(self, code, language, issues):
        """
        Generate smart contract improvement recommendations based on issues found and platform-specific best practices
        """
        recommendations = []
        
        # Platform-specific recommendations
        platform_recommendations = self.get_platform_specific_recommendations(language, issues)
        recommendations.extend(platform_recommendations)
        
        # Issue-specific recommendations
        issue_recommendations = self.get_issue_specific_recommendations(issues)
        recommendations.extend(issue_recommendations)
        
        # Best practices recommendations
        best_practices = self.get_best_practices_recommendations(language)
        recommendations.extend(best_practices)
        
        return list(set(recommendations))  # Remove duplicates
    
    def get_platform_specific_recommendations(self, language, issues):
        """Get platform-specific recommendations based on language and issues"""
        recommendations = []
        
        if language == "solidity":
            if any(i.get('type') == 'reentrancy' for i in issues):
                recommendations.append("Implement the checks-effects-interactions pattern to prevent reentrancy attacks")
                recommendations.append("Consider using OpenZeppelin's ReentrancyGuard")
            
            if any(i.get('type') == 'access-control' for i in issues):
                recommendations.append("Implement role-based access control using OpenZeppelin's AccessControl")
                recommendations.append("Use OpenZeppelin's Ownable for simple ownership-based access control")
            
            if any(i.get('type') == 'arithmetic' for i in issues):
                recommendations.append("Use SafeMath or Solidity 0.8+ for arithmetic operations")
                recommendations.append("Consider using OpenZeppelin's SafeMath for older Solidity versions")
            
        elif language == "pyteal":
            if any(i.get('type') == 'atomic' for i in issues):
                recommendations.append("Use atomic transfers for operations that must succeed together")
                recommendations.append("Implement proper transaction grouping for atomic operations")
            
            if any(i.get('type') == 'input-validation' for i in issues):
                recommendations.append("Validate all inputs using PyTeal's assertion functions")
                recommendations.append("Implement proper bounds checking for numeric inputs")
            
            if any(i.get('type') == 'state-management' for i in issues):
                recommendations.append("Use local state for contract-specific data")
                recommendations.append("Implement proper state initialization checks")
            
        elif language == "move":
            if any(i.get('type') == 'resource-safety' for i in issues):
                recommendations.append("Ensure resources cannot be duplicated or lost")
                recommendations.append("Use Move's resource types for proper ownership semantics")
            
            if any(i.get('type') == 'formal-verification' for i in issues):
                recommendations.append("Use the Move Prover to formally verify critical properties")
                recommendations.append("Implement invariant checks for critical state transitions")
            
            if any(i.get('type') == 'module-safety' for i in issues):
                recommendations.append("Use Move's module system for proper encapsulation")
                recommendations.append("Implement proper access control using Move's visibility modifiers")
            
        elif language == "rust":
            if any(i.get('type') == 'memory-safety' for i in issues):
                recommendations.append("Avoid unsafe blocks in smart contract code")
                recommendations.append("Use Rust's ownership system for memory safety")
            
            if any(i.get('type') == 'error-handling' for i in issues):
                recommendations.append("Use Result and Option types for robust error handling")
                recommendations.append("Implement proper error propagation and recovery")
            
            if any(i.get('type') == 'concurrency' for i in issues):
                recommendations.append("Use Rust's concurrency primitives safely")
                recommendations.append("Implement proper synchronization mechanisms")
        
        return recommendations
    
    def get_issue_specific_recommendations(self, issues):
        """Get recommendations specific to the issues found"""
        recommendations = []
        
        for issue in issues:
            if issue.get('type') == 'reentrancy':
                recommendations.append("Implement proper state management to prevent reentrancy")
            elif issue.get('type') == 'access-control':
                recommendations.append("Implement proper access control mechanisms")
            elif issue.get('type') == 'input-validation':
                recommendations.append("Validate all external inputs")
            elif issue.get('type') == 'arithmetic':
                recommendations.append("Use safe arithmetic operations")
            elif issue.get('type') == 'state-management':
                recommendations.append("Implement proper state management")
            elif issue.get('type') == 'resource-safety':
                recommendations.append("Ensure proper resource management")
            elif issue.get('type') == 'formal-verification':
                recommendations.append("Implement formal verification")
            elif issue.get('type') == 'module-safety':
                recommendations.append("Ensure proper module safety")
            elif issue.get('type') == 'memory-safety':
                recommendations.append("Ensure proper memory safety")
            elif issue.get('type') == 'error-handling':
                recommendations.append("Implement proper error handling")
            elif issue.get('type') == 'concurrency':
                recommendations.append("Ensure proper concurrency handling")
        
        return recommendations
    
    def get_best_practices_recommendations(self, language):
        """Get general best practices recommendations for the language"""
        recommendations = []
        
        if language == "solidity":
            recommendations.extend([
                "Follow the Solidity style guide",
                "Use events for important state changes",
                "Implement proper upgrade patterns",
                "Use immutable variables where possible",
                "Implement proper gas optimization patterns"
            ])
        elif language == "pyteal":
            recommendations.extend([
                "Follow PyTeal best practices",
                "Use proper transaction grouping",
                "Implement proper state management",
                "Use proper error handling",
                "Implement proper gas optimization"
            ])
        elif language == "move":
            recommendations.extend([
                "Follow Move best practices",
                "Use proper resource management",
                "Implement proper module safety",
                "Use proper error handling",
                "Implement proper formal verification"
            ])
        elif language == "rust":
            recommendations.extend([
                "Follow Rust best practices",
                "Use proper memory safety",
                "Implement proper error handling",
                "Use proper concurrency patterns",
                "Implement proper gas optimization"
            ])
        
        return recommendations
    
    def generate_property(self, code):
        """
        Generate a formal verification property based on code analysis
        """
        # This would use an LLM in production to generate specific properties
        return "assert forall n: uint256, balance(n) >= 0"
    
    def generate_spec(self, path, property):
        """
        Generate an SMT spec for Z3 verification
        """
        # Create a simple Z3 specification
        spec = f"""
        (declare-const balance (Array Int Int))
        (assert (forall ((n Int)) (>= (select balance n) 0)))
        (check-sat)
        """
        return spec
    
    def explain_vulnerability(self, code):
        """
        Explain a vulnerability in the code
        """
        # This would use an LLM in production
        return "This code contains potential vulnerabilities that could be exploited." 