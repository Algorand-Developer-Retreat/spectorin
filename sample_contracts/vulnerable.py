from pyteal import *

def vulnerable_program():
    # Vulnerability: No sender validation
    handle_creation = Return(Int(1))
    
    # Global storage for owner
    owner_key = Bytes("owner")
    balance_key = Bytes("balance")
    
    # Deposit funds
    deposit = Seq([
        App.globalPut(balance_key, App.globalGet(balance_key) + Txn.amount()),
        Return(Int(1))
    ])
    
    # Withdraw funds - vulnerability: no access control
    withdraw = Seq([
        # No check for Txn.sender() == App.globalGet(owner_key)
        InnerTxnBuilder.Begin(),
        InnerTxnBuilder.SetFields({
            TxnField.type_enum: TxnType.Payment,
            TxnField.receiver: Txn.sender(),
            TxnField.amount: App.globalGet(balance_key),
        }),
        InnerTxnBuilder.Submit(),
        App.globalPut(balance_key, Int(0)),
        Return(Int(1))
    ])
    
    program = Cond(
        [Txn.application_id() == Int(0), handle_creation],
        [Txn.on_completion() == OnComplete.DeleteApplication, Return(Int(0))],
        [Txn.application_args[0] == Bytes("deposit"), deposit],
        [Txn.application_args[0] == Bytes("withdraw"), withdraw]
    )
    
    return program

# Compile to TEAL
if __name__ == "__main__":
    print(compileTeal(vulnerable_program(), Mode.Application, version=6)) 