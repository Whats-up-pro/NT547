"""
Integration tests for the complete CFG pipeline
"""

import unittest
import sys
import os
import tempfile

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from cfg_visualizer.parser import SolidityParser
from cfg_visualizer.analyzer import CFGAnalyzer
from cfg_visualizer.visualizer import CFGVisualizer


class TestIntegration(unittest.TestCase):
    """Integration tests for the complete pipeline."""
    
    def test_complete_pipeline(self):
        """Test the complete analysis pipeline."""
        # Sample contract
        source = """
        contract TestContract {
            function transfer(address to, uint amount) public returns (bool) {
                require(balance >= amount);
                balance -= amount;
                return true;
            }
        }
        """
        
        # Parse
        parser = SolidityParser(source)
        parsed = parser.parse()
        
        self.assertGreater(len(parsed['functions']), 0)
        
        # Analyze
        analyzer = CFGAnalyzer()
        cfg_data = analyzer.analyze_function(
            parsed['functions'][0]['body'],
            parsed['functions'][0]['name']
        )
        
        self.assertIn('nodes', cfg_data)
        self.assertIn('edges', cfg_data)
        self.assertGreater(len(cfg_data['nodes']), 0)
    
    def test_multiple_functions(self):
        """Test analyzing multiple functions."""
        source = """
        contract MultiFunction {
            function foo() public {
                uint x = 1;
            }
            
            function bar() public {
                uint y = 2;
            }
        }
        """
        
        parser = SolidityParser(source)
        parsed = parser.parse()
        
        self.assertEqual(len(parsed['functions']), 2)
        
        analyzer = CFGAnalyzer()
        cfg_list = []
        
        for func in parsed['functions']:
            cfg = analyzer.analyze_function(func['body'], func['name'])
            cfg_list.append(cfg)
        
        self.assertEqual(len(cfg_list), 2)


if __name__ == '__main__':
    unittest.main()
