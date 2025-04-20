# spectorin/core/test/test_z3_pipeline.py

from spectorin.core.z3.constraint_builder import Z3ConstraintBuilder
from spectorin.core.analyzers.solidity.solidity_constraint_adapter import SolidityToZ3Adapter

def test_z3_solidity_pipeline():
    sample_ast = [
        {"type": "Assignment", "left": "x", "right": 5},         # ✅ int
        {"type": "Assignment", "left": "y", "right": "x"},
        {"type": "Assert", "condition": {"op": ">=", "left": "y", "right": 0}},  # ✅ int
    ]


    adapter = SolidityToZ3Adapter()
    ir = adapter.translate(sample_ast)

    builder = Z3ConstraintBuilder()
    builder.from_solidity_ast(ir)

    result = builder.check()
    assert str(result) == "sat"

    model = builder.model()
    print("🧠 SAT Model:", model)
