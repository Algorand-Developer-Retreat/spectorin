from pyteal import *

def approval_program():
    # Global state keys
    counter_key = Bytes("counter")
    owner_key = Bytes("owner")

    # Initialize counter
    init_counter = Seq([
        App.globalPut(counter_key, Int(0)),
        App.globalPut(owner_key, Txn.sender()),
        Return(Int(1))
    ])

    # Increment counter
    increment = Seq([
        App.globalPut(counter_key, App.globalGet(counter_key) + Int(1)),
        Return(Int(1))
    ])

    # Transfer funds
    transfer_funds = Seq([
        InnerTxnBuilder.Begin(),
        InnerTxnBuilder.SetFields({
            TxnField.type_enum: TxnType.Payment,
            TxnField.amount: Btoi(Txn.application_args[1]),
            TxnField.receiver: Txn.accounts[1]
        }),
        InnerTxnBuilder.Execute(),
        Return(Int(1))
    ])

    # Main router
    program = Cond(
        [Txn.application_id() == Int(0), init_counter],
        [Txn.application_args[0] == Bytes("increment"), increment],
        [Txn.application_args[0] == Bytes("transfer"), transfer_funds]
    )

    return program

def clear_state_program():
    return Return(Int(1))

if __name__ == "__main__":
    with open("approval.teal", "w") as f:
        compiled = compileTeal(approval_program(), mode=Mode.Application, version=6)
        f.write(compiled)

    with open("clear.teal", "w") as f:
        compiled = compileTeal(clear_state_program(), mode=Mode.Application, version=6)
        f.write(compiled) 