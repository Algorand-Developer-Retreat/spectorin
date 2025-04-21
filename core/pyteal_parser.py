# core/pyteal_parser.py

from pyteal import Pop, Int, Seq, Assert, BinaryExpr, TealOp, Expr
# from pyteal.ast.pop import Pop  # import the AST Pop class directly

def parse_pyteal_contract(program):
    """
    Parse the given PyTeal program (a Seq) into a simplified AST format
    that can be translated to Z3 IR.
    """
    ast = []

    if not isinstance(program, Seq):
        raise ValueError("Program must be a Seq of statements")

    for stmt in program.args:
        cls = stmt.__class__.__name__

        if cls == "Int":
            ast.append({
                "type": "Assignment",
                "left": "var",        # default var name; you can enhance this later
                "right": stmt.value
            })

        elif cls == "Assert":
            # stmt.cond holds the inner expression
            condition = parse_expression(stmt.cond)
            ast.append({
                "type": "Assert",
                "condition": condition
            })

        elif cls == "Pop":
            # Pop(expr) stores the expression in stmt.expr
            value = parse_expression(stmt.expr)
            ast.append({
                "type": "Pop",
                "value": value
            })
            
        elif cls == "UnaryExpr":
            # Handle the UnaryExpr created by Pop(x)
            # In PyTeal, when you call Pop(x), you get a UnaryExpr
            if hasattr(stmt, 'op') and stmt.op.__class__.__name__ == "Pop":
                # Extract the expression being popped
                if hasattr(stmt, 'expr'):
                    value = parse_expression(stmt.expr)
                else:
                    # Fallback for different attribute structure
                    value = parse_expression(stmt.arg)
                
                ast.append({
                    "type": "Pop",
                    "value": value
                })
            else:
                # Handle other unary expressions here if needed
                raise ValueError(f"Unsupported unary operation: {stmt.op.__class__.__name__}")

        else:
            raise ValueError(f"Unknown PyTeal statement type: {cls}")

    return ast


def parse_expression(expr):
    """
    Recursively parse PyTeal expressions into a dict or literal that
    can be fed into the Z3 adapter.
    """
    from pyteal import TealOp

    cls = expr.__class__.__name__
    
    if cls == "Int":
        return expr.value

    if isinstance(expr, BinaryExpr):
        left = parse_expression(expr.left)
        right = parse_expression(expr.right)
        op = expr.op

        # Map TealOp to IR node
        op_map = {
            TealOp.Add: "Add",
            TealOp.Subtract: "Subtract",
            TealOp.Multiply: "Multiply",
            TealOp.GreaterThanEqual: "GreaterThanEqual",
            TealOp.LessThanEqual: "LessThanEqual",
            TealOp.Equal: "Equal"
        }
        if op in op_map:
            return {"type": op_map[op], "left": left, "right": right}

        raise ValueError(f"Unsupported operator: {op}")

    # Handle BinaryExpr objects based on class name if the above check fails
    if cls.endswith("Expr"):
        if hasattr(expr, 'left') and hasattr(expr, 'right'):
            left = parse_expression(expr.left)
            right = parse_expression(expr.right)
            
            # Try to determine operation type from class name
            if "Add" in cls:
                return {"type": "Add", "left": left, "right": right}
            elif "Subtract" in cls:
                return {"type": "Subtract", "left": left, "right": right}
            elif "Multiply" in cls:
                return {"type": "Multiply", "left": left, "right": right}
            elif "Greater" in cls and "Equal" in cls:
                return {"type": "GreaterThanEqual", "left": left, "right": right}
            elif "Less" in cls and "Equal" in cls:
                return {"type": "LessThanEqual", "left": left, "right": right}
            elif "Equal" in cls:
                return {"type": "Equal", "left": left, "right": right}

    raise ValueError(f"Unsupported PyTeal Expr type: {cls}")
