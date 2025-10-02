// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/**
 * Auction Contract
 * Demonstrates complex control flow patterns
 */
contract Auction {
    address public beneficiary;
    uint256 public auctionEndTime;
    address public highestBidder;
    uint256 public highestBid;
    bool public ended;
    
    mapping(address => uint256) public pendingReturns;
    
    constructor(uint256 biddingTime, address beneficiaryAddress) {
        beneficiary = beneficiaryAddress;
        auctionEndTime = block.timestamp + biddingTime;
    }
    
    function bid() public payable {
        require(block.timestamp <= auctionEndTime, "Auction already ended");
        require(msg.value > highestBid, "Bid not high enough");
        
        if (highestBid != 0) {
            pendingReturns[highestBidder] += highestBid;
        }
        
        highestBidder = msg.sender;
        highestBid = msg.value;
    }
    
    function withdraw() public returns (bool) {
        uint256 amount = pendingReturns[msg.sender];
        
        if (amount > 0) {
            pendingReturns[msg.sender] = 0;
            
            if (!payable(msg.sender).send(amount)) {
                pendingReturns[msg.sender] = amount;
                return false;
            }
        }
        
        return true;
    }
    
    function auctionEnd() public {
        require(block.timestamp >= auctionEndTime, "Auction not yet ended");
        require(!ended, "Auction already ended");
        
        ended = true;
        payable(beneficiary).transfer(highestBid);
    }
}
