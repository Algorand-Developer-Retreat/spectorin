from pyteal import Int, Seq, Assert, Pop

def parse_pyteal_contract(program):
    """
    Parse the given PyTeal program into a simplified AST format
    that can be translated to Z3 IR.
    """
    ast = []

    if isinstance(program, Seq):
        for stmt in program.args:
            if isinstance(stmt, Int):
                ast.append({
                    "type": "Assignment",
                    "left": "var",  # Default var name
                    "right": stmt.value
                })
            elif isinstance(stmt, Assert):
                ast.append({
                    "type": "Assert",
                    "condition": stmt.cond  # Use stmt.cond for assert condition
                })
            elif hasattr(stmt, 'type') and stmt.type == 'Pop':  # Ensure Pop is handled
                ast.append({
                    "type": "Pop",
                    "var": stmt.args[0]  # Assuming stmt.args[0] holds the variable
                })
    return ast
