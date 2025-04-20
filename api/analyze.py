# api/analyze.py (example usage)

from core.plugin_manager import get_plugin_manager

def analyze_code(code):
    ast_tree = parse_to_ast(code)  # however you parse your code

    plugin_manager = get_plugin_manager()

    # Call all plugins that implement analyze_ast
    results = plugin_manager.hook.analyze_ast(ast_tree=ast_tree)
    
    return results
