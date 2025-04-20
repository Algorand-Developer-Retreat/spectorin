# spectorin/core/analyzers/solidity/solidity_constraint_adapter.py

from typing import List, Dict, Any

class SolidityToZ3Adapter:
    """
    Translates simplified Solidity AST to intermediate format
    understood by Z3ConstraintBuilder.
    """

    def __init__(self):
        self.ir = []  # Intermediate representation list

    def translate(self, ast: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        for node in ast:
            if node["type"] == "Assignment":
                right = node["right"]
                if isinstance(right, str) and right.isdigit():
                    right = int(right)
                self.ir.append({
                    "type": "assignment",
                    "left": node["left"],
                    "right": right
                })
            elif node["type"] == "Assert":
                self.ir.append({
                    "type": "assert",
                    "condition": node["condition"]
                })
        return self.ir

