from pyteal import Int, Txn, Seq, Assert, Pop, Global

def approval_program():
    # Simple counter program with a vulnerability (no sender check)
    counter = Int(0)
    
    increment_counter = Seq([
        # Vulnerability: No Txn.sender check for authorization
        counter := counter + Int(1),
        Pop(counter)
    ])
    
    check_value = Seq([
        Assert(counter >= Int(0))
    ])
    
    program = Seq([
        increment_counter,
        check_value
    ])
    
    return program

# Compile this with PyTeal to get TEAL code 