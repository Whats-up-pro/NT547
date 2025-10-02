// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/**
 * Voting Contract
 * Demonstrates complex control flow with multiple conditions and state changes
 */
contract Voting {
    struct Proposal {
        string description;
        uint256 voteCount;
        bool executed;
        uint256 deadline;
    }
    
    mapping(uint256 => Proposal) public proposals;
    mapping(address => mapping(uint256 => bool)) public hasVoted;
    uint256 public proposalCount;
    address public admin;
    
    constructor() {
        admin = msg.sender;
    }
    
    function createProposal(string memory _description, uint256 _duration) public {
        require(msg.sender == admin, "Only admin can create proposals");
        require(bytes(_description).length > 0, "Description cannot be empty");
        
        uint256 proposalId = proposalCount;
        proposals[proposalId] = Proposal({
            description: _description,
            voteCount: 0,
            executed: false,
            deadline: block.timestamp + _duration
        });
        
        proposalCount++;
    }
    
    function vote(uint256 _proposalId) public {
        require(_proposalId < proposalCount, "Invalid proposal ID");
        require(!hasVoted[msg.sender][_proposalId], "Already voted");
        
        Proposal storage proposal = proposals[_proposalId];
        require(block.timestamp < proposal.deadline, "Voting period has ended");
        require(!proposal.executed, "Proposal already executed");
        
        proposal.voteCount++;
        hasVoted[msg.sender][_proposalId] = true;
    }
    
    function executeProposal(uint256 _proposalId) public {
        require(msg.sender == admin, "Only admin can execute");
        require(_proposalId < proposalCount, "Invalid proposal ID");
        
        Proposal storage proposal = proposals[_proposalId];
        require(block.timestamp >= proposal.deadline, "Voting period not ended");
        require(!proposal.executed, "Already executed");
        
        if (proposal.voteCount > 0) {
            proposal.executed = true;
        } else {
            revert("Not enough votes");
        }
    }
}
