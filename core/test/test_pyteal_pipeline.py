import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))


from pyteal import *
from core.z3.smart_contract_to_z3_adapter import SmartContractToZ3Adapter

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
