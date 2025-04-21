# core/test/test_pyteal_pipeline.py

import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from pyteal import Pop, Int, Seq, Assert
# from pyteal.ast.pop import Pop # type: ignore

from core.z3.smart_contract_adapter import SmartContractToZ3Adapter

def test_pyteal_translation():
    x = Int(5)
    y = x + Int(3)
    program = Seq([
        Pop(x),
        Pop(y),
        Assert(y >= Int(0))
    ])
    
    adapter = SmartContractToZ3Adapter()
    ir = adapter.translate(program, contract_type="pyteal")
    
    print("🔍 Z3 IR from PyTeal:", ir)
    assert len(ir) > 0

def test_pyteal_translation_complex():
    x = Int(5)
    y = x * Int(2)
    z = y + Int(3)
    program = Seq([
        Pop(x),
        Pop(y),
        Pop(z),
        Assert(z >= Int(10))
    ])
    
    adapter = SmartContractToZ3Adapter()
    ir = adapter.translate(program, contract_type="pyteal")
    
    print("🔍 Z3 IR from PyTeal (Complex):", ir)
    assert len(ir) > 0
