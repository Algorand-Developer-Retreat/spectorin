// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract VulnerableWallet {
    address public owner;
    mapping(address => uint256) public balances;
    
    constructor() {
        owner = msg.sender;
    }
    
    modifier onlyOwner() {
        // Vulnerability: Using tx.origin instead of msg.sender
        require(tx.origin == owner, "Not owner");
        _;
    }
    
    function deposit() public payable {
        balances[msg.sender] += msg.value;
    }
    
    function withdrawAll() public onlyOwner {
        // Vulnerability: Reentrancy vulnerability
        (bool success, ) = msg.sender.call{value: address(this).balance}("");
        balances[msg.sender] = 0; // State updated after external call
    }
    
    function transfer(address _to, uint256 _amount) public {
        // No check for sufficient balance
        balances[msg.sender] -= _amount;
        balances[_to] += _amount;
    }
} 