// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/**
 * Simple Token Contract
 * Demonstrates basic control flow with require statements
 */
contract SimpleToken {
    mapping(address => uint256) public balances;
    uint256 public totalSupply;
    address public owner;
    
    constructor(uint256 _initialSupply) {
        owner = msg.sender;
        balances[msg.sender] = _initialSupply;
        totalSupply = _initialSupply;
    }
    
    function transfer(address _to, uint256 _amount) public returns (bool) {
        require(_to != address(0), "Invalid address");
        require(balances[msg.sender] >= _amount, "Insufficient balance");
        
        balances[msg.sender] -= _amount;
        balances[_to] += _amount;
        
        return true;
    }
    
    function mint(address _to, uint256 _amount) public returns (bool) {
        require(msg.sender == owner, "Only owner can mint");
        require(_to != address(0), "Invalid address");
        
        balances[_to] += _amount;
        totalSupply += _amount;
        
        return true;
    }
}
