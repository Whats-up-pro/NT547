// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/**
 * Simple Token Contract
 * A basic ERC20-like token for demonstration
 */
contract SimpleToken {
    mapping(address => uint256) public balances;
    address public owner;
    
    constructor() {
        owner = msg.sender;
        balances[owner] = 1000000;
    }
    
    function transfer(address to, uint256 amount) public returns (bool) {
        require(balances[msg.sender] >= amount, "Insufficient balance");
        require(to != address(0), "Invalid address");
        
        balances[msg.sender] -= amount;
        balances[to] += amount;
        
        return true;
    }
    
    function mint(address to, uint256 amount) public {
        require(msg.sender == owner, "Only owner can mint");
        balances[to] += amount;
    }
    
    function getBalance(address account) public view returns (uint256) {
        return balances[account];
    }
}
