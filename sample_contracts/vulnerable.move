module VulnerableToken {
    struct Coin has key {
        value: u64,
    }

    // Vulnerability: No access control for admin functions
    public fun mint(addr: address, amount: u64) {
        let coin = borrow_global_mut<Coin>(addr);
        // Minting without any authorization check
        coin.value = coin.value + amount;
    }

    // Vulnerability: No checking for sufficient funds
    public fun transfer(from: address, to: address, amount: u64) {
        let from_coin = borrow_global_mut<Coin>(from);
        // No check if from_coin.value >= amount
        from_coin.value = from_coin.value - amount; // Potential underflow

        let to_coin = borrow_global_mut<Coin>(to);
        to_coin.value = to_coin.value + amount;
    }

    // Vulnerability: Resource could be lost
    public fun burn(addr: address) {
        let coin = move_from<Coin>(addr);
        // Resource is dropped without proper cleanup
    }
} 