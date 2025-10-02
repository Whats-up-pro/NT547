// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/**
 * Voting Contract
 * Demonstrates control flow with loops and conditions
 */
contract Voting {
    struct Proposal {
        string description;
        uint256 voteCount;
        bool executed;
    }
    
    mapping(address => bool) public hasVoted;
    mapping(uint256 => Proposal) public proposals;
    uint256 public proposalCount;
    address public chairperson;
    
    constructor() {
        chairperson = msg.sender;
    }
    
    function createProposal(string memory description) public {
        require(msg.sender == chairperson, "Only chairperson can create proposals");
        
        proposals[proposalCount] = Proposal({
            description: description,
            voteCount: 0,
            executed: false
        });
        
        proposalCount++;
    }
    
    function vote(uint256 proposalId) public {
        require(!hasVoted[msg.sender], "Already voted");
        require(proposalId < proposalCount, "Invalid proposal");
        require(!proposals[proposalId].executed, "Proposal already executed");
        
        hasVoted[msg.sender] = true;
        proposals[proposalId].voteCount++;
    }
    
    function executeProposal(uint256 proposalId) public {
        require(msg.sender == chairperson, "Only chairperson can execute");
        require(proposalId < proposalCount, "Invalid proposal");
        require(!proposals[proposalId].executed, "Already executed");
        
        Proposal storage proposal = proposals[proposalId];
        
        if (proposal.voteCount > 10) {
            proposal.executed = true;
        }
    }
    
    function getWinningProposal() public view returns (uint256) {
        uint256 winningVoteCount = 0;
        uint256 winningProposal = 0;
        
        for (uint256 i = 0; i < proposalCount; i++) {
            if (proposals[i].voteCount > winningVoteCount) {
                winningVoteCount = proposals[i].voteCount;
                winningProposal = i;
            }
        }
        
        return winningProposal;
    }
}
