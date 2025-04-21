// examples/solidity_example.sol
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Vulnerable {
    uint public counter = 0;
    mapping(address => uint) public balances;
    
    // Vulnerability: Missing access control
    function increment() public {
        counter += 1;
    }
    
    // Vulnerability: Integer overflow possible in older Solidity versions
    function deposit() public payable {
        balances[msg.sender] += msg.value;
    }
    
    // Vulnerability: Reentrancy
    function withdraw(uint amount) public {
        require(balances[msg.sender] >= amount, "Insufficient balance");
        
        // Vulnerability: State update after external call
        (bool success, ) = msg.sender.call{value: amount}("");
        require(success, "Transfer failed");
        
        balances[msg.sender] -= amount;
    }
} 