"""
Solidity Parser Module
Parses Solidity smart contract source code and extracts AST.
"""

import re
from typing import Dict, List, Optional, Any
import json


class SolidityParser:
    """Parser for Solidity smart contracts."""
    
    def __init__(self, source_code: str):
        """
        Initialize the parser with source code.
        
        Args:
            source_code: Solidity source code as string
        """
        self.source_code = source_code
        self.contracts = []
        self.functions = []
        
    def parse(self) -> Dict[str, Any]:
        """
        Parse the Solidity source code and extract structure.
        
        Returns:
            Dictionary containing parsed contract information
        """
        result = {
            'contracts': [],
            'functions': [],
            'raw_code': self.source_code
        }
        
        # Extract contract declarations
        contract_pattern = r'contract\s+(\w+)\s*(?:is\s+[\w\s,]+)?\s*\{'
        contracts = re.finditer(contract_pattern, self.source_code)
        
        for match in contracts:
            contract_name = match.group(1)
            contract_start = match.start()
            
            # Find the end of the contract
            contract_end = self._find_matching_brace(contract_start)
            contract_body = self.source_code[contract_start:contract_end]
            
            contract_info = {
                'name': contract_name,
                'start': contract_start,
                'end': contract_end,
                'functions': self._extract_functions(contract_body)
            }
            
            result['contracts'].append(contract_info)
            result['functions'].extend(contract_info['functions'])
        
        self.contracts = result['contracts']
        self.functions = result['functions']
        
        return result
    
    def _find_matching_brace(self, start_pos: int) -> int:
        """Find the matching closing brace for an opening brace."""
        brace_count = 0
        in_brace = False
        
        for i in range(start_pos, len(self.source_code)):
            if self.source_code[i] == '{':
                brace_count += 1
                in_brace = True
            elif self.source_code[i] == '}':
                brace_count -= 1
                if brace_count == 0 and in_brace:
                    return i + 1
        
        return len(self.source_code)
    
    def _extract_functions(self, contract_body: str) -> List[Dict[str, Any]]:
        """Extract function definitions from contract body."""
        functions = []
        
        # Pattern for function declarations
        func_pattern = r'function\s+(\w+)\s*\([^)]*\)\s*(?:public|private|internal|external)?(?:\s+(?:pure|view|payable))?(?:\s+returns\s*\([^)]*\))?\s*\{'
        
        for match in re.finditer(func_pattern, contract_body):
            func_name = match.group(1)
            func_start = match.start()
            func_end = self._find_matching_brace_in_substring(contract_body, func_start)
            func_body = contract_body[func_start:func_end]
            
            functions.append({
                'name': func_name,
                'body': func_body,
                'start': func_start,
                'end': func_end
            })
        
        return functions
    
    def _find_matching_brace_in_substring(self, text: str, start_pos: int) -> int:
        """Find matching brace in a substring."""
        brace_count = 0
        in_brace = False
        
        for i in range(start_pos, len(text)):
            if text[i] == '{':
                brace_count += 1
                in_brace = True
            elif text[i] == '}':
                brace_count -= 1
                if brace_count == 0 and in_brace:
                    return i + 1
        
        return len(text)
    
    def get_functions(self) -> List[Dict[str, Any]]:
        """Get list of parsed functions."""
        return self.functions
    
    def get_contracts(self) -> List[Dict[str, Any]]:
        """Get list of parsed contracts."""
        return self.contracts
