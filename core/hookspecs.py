# core/hookspecs.py

import pluggy

hookspec = pluggy.HookspecMarker("spectorin")

class HookSpecs:
    @hookspec
    def analyze_ast(self, ast_tree):
        """Modify or analyze the AST and return metadata or issues."""
    
    @hookspec
    def register_custom_checks(self, checker_registry):
        """Register new checks into the checker registry."""
