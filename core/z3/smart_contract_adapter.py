# core/z3/smart_contract_adapter.py

from core.z3.constraint_builder import Z3ConstraintBuilder
from core.pyteal_parser import parse_pyteal_contract

class SmartContractToZ3Adapter:
    """
    Adapter that translates smart contract ASTs (Solidity or PyTeal)
    into Z3 constraints via the Z3ConstraintBuilder.
    """

    def __init__(self):
        self.builder = Z3ConstraintBuilder()

    def translate(self, program, contract_type="solidity"):
        """
        Dispatch to the correct parser + builder pipeline.
        """
        if contract_type == "pyteal":
            # Parse PyTeal Seq → our IR
            ir = parse_pyteal_contract(program)
        else:
            # fallback to Solidity (if implemented)
            ir = self.translate_solidity_ast(program)

        # Feed the intermediate IR into the Z3 builder
        self.builder.from_solidity_ast(ir)  # name kept from earlier; it's IR-driven, not just Solidity
        return ir
