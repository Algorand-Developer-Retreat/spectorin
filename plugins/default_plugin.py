# plugins/default_plugin.py

import pluggy
from core.hookspecs import HookSpecs

hookimpl = pluggy.HookimplMarker("spectorin")

class DefaultPlugin:
    @hookimpl
    def analyze_ast(self, ast_tree):
        return {"default_plugin_saw": ast_tree.__class__.__name__}

    @hookimpl
    def register_custom_checks(self, checker_registry):
        checker_registry.append("check-for-loops")  # example
