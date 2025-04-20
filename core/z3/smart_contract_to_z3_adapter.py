from core.analyzers.solidity.solidity_constraint_adapter import SolidityToZ3Adapter
from core.pyteal_parser import parse_pyteal_contract


class SmartContractToZ3Adapter:
    """
    Unified Adapter to convert any supported Smart Contract (Solidity, PyTeal, etc.)
    into a common Z3 Intermediate Representation (IR).
    """

    def __init__(self):
        self.ir = []

    def translate(self, contract, contract_type="solidity"):
        if contract_type == "solidity":
            return self._translate_solidity(contract)
        elif contract_type == "pyteal":
            return self._translate_pyteal(contract)
        else:
            raise ValueError(f"Unsupported contract type: {contract_type}")

    def _translate_solidity(self, ast):
        adapter = SolidityToZ3Adapter()
        return adapter.translate(ast)

    def _translate_pyteal(self, program):
        pyteal_ast = parse_pyteal_contract(program)
        self.ir.clear()

        for node in pyteal_ast:
            if node["type"] == "Assignment":
                self.ir.append({
                    "type": "assignment",
                    "left": node["left"],
                    "right": node["right"]
                })
            elif node["type"] == "Assert":
                self.ir.append({
                    "type": "assert",
                    "condition": node["condition"]
                })
        return self.ir
