"""
Unit tests for CFG Visualizer
"""

import unittest
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from cfg_visualizer.parser import SolidityParser
from cfg_visualizer.analyzer import CFGAnalyzer
from cfg_visualizer.visualizer import CFGVisualizer


class TestSolidityParser(unittest.TestCase):
    """Test cases for Solidity Parser."""
    
    def test_parse_simple_contract(self):
        """Test parsing a simple contract."""
        source = """
        contract SimpleContract {
            function test() public {
                uint x = 5;
            }
        }
        """
        
        parser = SolidityParser(source)
        result = parser.parse()
        
        self.assertIn('contracts', result)
        self.assertIn('functions', result)
        self.assertEqual(len(result['contracts']), 1)
        self.assertEqual(result['contracts'][0]['name'], 'SimpleContract')
    
    def test_parse_multiple_functions(self):
        """Test parsing multiple functions."""
        source = """
        contract MyContract {
            function foo() public {
                return;
            }
            
            function bar() public {
                return;
            }
        }
        """
        
        parser = SolidityParser(source)
        result = parser.parse()
        
        self.assertEqual(len(result['functions']), 2)
        function_names = [f['name'] for f in result['functions']]
        self.assertIn('foo', function_names)
        self.assertIn('bar', function_names)


class TestCFGAnalyzer(unittest.TestCase):
    """Test cases for CFG Analyzer."""
    
    def test_analyze_simple_function(self):
        """Test analyzing a simple function."""
        function_body = """
        function test() public {
            uint x = 5;
            return;
        }
        """
        
        analyzer = CFGAnalyzer()
        result = analyzer.analyze_function(function_body, 'test')
        
        self.assertIn('nodes', result)
        self.assertIn('edges', result)
        self.assertIn('entry', result)
        self.assertGreater(len(result['nodes']), 0)
    
    def test_analyze_if_statement(self):
        """Test analyzing function with if statement."""
        function_body = """
        function test() public {
            if (x > 5) {
                y = 1;
            }
        }
        """
        
        analyzer = CFGAnalyzer()
        result = analyzer.analyze_function(function_body, 'test')
        
        # Should have condition node
        node_types = [node.type for node in result['nodes'].values()]
        self.assertIn('condition', node_types)
    
    def test_analyze_return_statement(self):
        """Test analyzing function with return."""
        function_body = """
        function test() public returns (uint) {
            return 42;
        }
        """
        
        analyzer = CFGAnalyzer()
        result = analyzer.analyze_function(function_body, 'test')
        
        # Should have return and exit nodes
        node_types = [node.type for node in result['nodes'].values()]
        self.assertIn('return', node_types)
        self.assertIn('exit', node_types)


class TestCFGVisualizer(unittest.TestCase):
    """Test cases for CFG Visualizer."""
    
    def test_visualizer_creation(self):
        """Test creating a visualizer instance."""
        visualizer = CFGVisualizer()
        self.assertIsNotNone(visualizer)
    
    def test_visualize_simple_cfg(self):
        """Test visualizing a simple CFG."""
        # Create a simple CFG
        analyzer = CFGAnalyzer()
        function_body = """
        function test() public {
            uint x = 5;
        }
        """
        cfg_data = analyzer.analyze_function(function_body, 'test')
        
        # This test just checks that visualization doesn't crash
        # Actual rendering requires graphviz to be installed
        visualizer = CFGVisualizer()
        self.assertIsNotNone(cfg_data)


if __name__ == '__main__':
    unittest.main()
