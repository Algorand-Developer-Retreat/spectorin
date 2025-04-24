# core/pyteal_parser.py

from pyteal import Pop, Int, Seq, Assert, BinaryExpr, TealOp, Expr, UnaryExpr
from typing import Dict, Any, List, Union
import logging

logger = logging.getLogger(__name__)

def parse_pyteal_contract(program: Seq) -> List[Dict[str, Any]]:
    """
    Parse the given PyTeal program (a Seq) into a simplified AST format
    that can be translated to Z3 IR.
    
    Args:
        program: A PyTeal Seq object containing the program statements
        
    Returns:
        List of dictionaries representing the AST nodes
        
    Raises:
        ValueError: If the program is not a valid PyTeal Seq
    """
    ast = []

    if not isinstance(program, Seq):
        raise ValueError("Program must be a Seq of statements")

    try:
        for stmt in program.args:
            cls = stmt.__class__.__name__
            
            if cls == "Int":
                ast.append({
                    "type": "Assignment",
                    "left": "var",
                    "right": stmt.value,
                    "line": getattr(stmt, 'line', None)
                })

            elif cls == "Assert":
                condition = parse_expression(stmt.cond)
                ast.append({
                    "type": "Assert",
                    "condition": condition,
                    "line": getattr(stmt, 'line', None)
                })

            elif cls == "Pop":
                value = parse_expression(stmt.expr)
                ast.append({
                    "type": "Pop",
                    "value": value,
                    "line": getattr(stmt, 'line', None)
                })
                
            elif cls == "UnaryExpr":
                if hasattr(stmt, 'op') and stmt.op.__class__.__name__ == "Pop":
                    value = parse_expression(stmt.expr if hasattr(stmt, 'expr') else stmt.arg)
                    ast.append({
                        "type": "Pop",
                        "value": value,
                        "line": getattr(stmt, 'line', None)
                    })
                else:
                    logger.warning(f"Unsupported unary operation: {stmt.op.__class__.__name__}")
                    continue

            else:
                logger.warning(f"Unknown PyTeal statement type: {cls}")
                continue

    except Exception as e:
        logger.error(f"Error parsing PyTeal program: {str(e)}")
        raise ValueError(f"Failed to parse PyTeal program: {str(e)}")

    return ast

def parse_expression(expr: Expr) -> Union[Dict[str, Any], int]:
    """
    Recursively parse PyTeal expressions into a dict or literal that
    can be fed into the Z3 adapter.
    
    Args:
        expr: A PyTeal expression to parse
        
    Returns:
        Either a dictionary representing the expression or a literal value
        
    Raises:
        ValueError: If the expression type is not supported
    """
    from pyteal import TealOp

    cls = expr.__class__.__name__
    
    if cls == "Int":
        return expr.value

    if isinstance(expr, BinaryExpr):
        try:
            left = parse_expression(expr.left)
            right = parse_expression(expr.right)
            op = expr.op

            op_map = {
                TealOp.Add: "Add",
                TealOp.Subtract: "Subtract",
                TealOp.Multiply: "Multiply",
                TealOp.Divide: "Divide",
                TealOp.Modulo: "Modulo",
                TealOp.GreaterThanEqual: "GreaterThanEqual",
                TealOp.LessThanEqual: "LessThanEqual",
                TealOp.Equal: "Equal",
                TealOp.NotEqual: "NotEqual",
                TealOp.GreaterThan: "GreaterThan",
                TealOp.LessThan: "LessThan",
                TealOp.And: "And",
                TealOp.Or: "Or"
            }
            
            if op in op_map:
                return {
                    "type": op_map[op],
                    "left": left,
                    "right": right,
                    "line": getattr(expr, 'line', None)
                }

            logger.warning(f"Unsupported operator: {op}")
            return {"type": "Unknown", "left": left, "right": right}

        except Exception as e:
            logger.error(f"Error parsing binary expression: {str(e)}")
            raise ValueError(f"Failed to parse binary expression: {str(e)}")

    if cls.endswith("Expr"):
        try:
            if hasattr(expr, 'left') and hasattr(expr, 'right'):
                left = parse_expression(expr.left)
                right = parse_expression(expr.right)
                
                op_map = {
                    "Add": "Add",
                    "Subtract": "Subtract",
                    "Multiply": "Multiply",
                    "Divide": "Divide",
                    "Modulo": "Modulo",
                    "GreaterThanEqual": "GreaterThanEqual",
                    "LessThanEqual": "LessThanEqual",
                    "Equal": "Equal",
                    "NotEqual": "NotEqual",
                    "GreaterThan": "GreaterThan",
                    "LessThan": "LessThan",
                    "And": "And",
                    "Or": "Or"
                }
                
                for op_name, op_type in op_map.items():
                    if op_name in cls:
                        return {
                            "type": op_type,
                            "left": left,
                            "right": right,
                            "line": getattr(expr, 'line', None)
                        }
                
                logger.warning(f"Unknown expression type: {cls}")
                return {"type": "Unknown", "left": left, "right": right}

        except Exception as e:
            logger.error(f"Error parsing expression: {str(e)}")
            raise ValueError(f"Failed to parse expression: {str(e)}")

    logger.warning(f"Unsupported PyTeal Expr type: {cls}")
    raise ValueError(f"Unsupported PyTeal Expr type: {cls}")
