module MyToken {
    struct Coin has key {
        value: u64,
    }

    // Vulnerability: No access control
    public fun transfer(from: address, to: address, amount: u64) {
        let coin = borrow_global_mut<Coin>(from);
        
        // Vulnerability: No check for sufficient balance
        coin.value = coin.value - amount;
        
        let recipient_coin = borrow_global_mut<Coin>(to);
        recipient_coin.value = recipient_coin.value + amount;
    }

    // Vulnerability: Resource could be lost
    public fun burn(addr: address) {
        let coin = move_from<Coin>(addr);
        // Coin is implicitly dropped without handling
    }
} 