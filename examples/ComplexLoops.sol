// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/**
 * Complex Loops Contract
 * Demonstrates various loop structures and nested conditions
 */
contract ComplexLoops {
    uint256[] public data;
    
    function processWithFor(uint256 limit) public returns (uint256) {
        uint256 sum = 0;
        
        for (uint256 i = 0; i < limit; i++) {
            if (i % 2 == 0) {
                sum += i;
            } else {
                sum -= i;
            }
        }
        
        return sum;
    }
    
    function processWithWhile(uint256 limit) public returns (uint256) {
        uint256 sum = 0;
        uint256 i = 0;
        
        while (i < limit) {
            if (sum > 100) {
                break;
            }
            sum += i;
            i++;
        }
        
        return sum;
    }
    
    function nestedLoops(uint256 rows, uint256 cols) public returns (uint256) {
        uint256 result = 0;
        
        for (uint256 i = 0; i < rows; i++) {
            for (uint256 j = 0; j < cols; j++) {
                if (i == j) {
                    result += i * j;
                } else if (i > j) {
                    result += i;
                } else {
                    result += j;
                }
            }
        }
        
        return result;
    }
    
    function doWhileExample(uint256 start) public pure returns (uint256) {
        uint256 result = start;
        
        do {
            result = result * 2;
            if (result > 1000) {
                break;
            }
        } while (result < 100);
        
        return result;
    }
}
