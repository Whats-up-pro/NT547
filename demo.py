#!/usr/bin/env python3
"""
Demo script to test the CFG Visualizer
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from cfg_visualizer.parser import SolidityParser
from cfg_visualizer.analyzer import CFGAnalyzer
from cfg_visualizer.visualizer import CFGVisualizer


def demo_simple_token():
    """Demo with SimpleToken contract."""
    print("=" * 60)
    print("Demo: SimpleToken Contract")
    print("=" * 60)
    
    # Read the contract
    contract_path = 'examples/SimpleToken.sol'
    
    if not os.path.exists(contract_path):
        print(f"Error: {contract_path} not found")
        return
    
    with open(contract_path, 'r') as f:
        source_code = f.read()
    
    # Parse
    print("\n1. Parsing contract...")
    parser = SolidityParser(source_code)
    parsed = parser.parse()
    
    print(f"   Found {len(parsed['contracts'])} contract(s)")
    print(f"   Found {len(parsed['functions'])} function(s)")
    
    for func in parsed['functions']:
        print(f"   - {func['name']}")
    
    # Analyze
    print("\n2. Analyzing control flow...")
    analyzer = CFGAnalyzer()
    cfg_list = []
    
    for func in parsed['functions']:
        print(f"   Analyzing: {func['name']}")
        cfg = analyzer.analyze_function(func['body'], func['name'])
        cfg_list.append(cfg)
        print(f"     Nodes: {len(cfg['nodes'])}, Edges: {len(cfg['edges'])}")
    
    # Visualize
    print("\n3. Creating visualizations...")
    visualizer = CFGVisualizer()
    
    # Create output directory
    os.makedirs('output', exist_ok=True)
    
    for cfg in cfg_list:
        func_name = cfg['function_name']
        output_file = f'output/cfg_{func_name}'
        
        try:
            # Note: This requires graphviz to be installed
            path = visualizer.visualize(cfg, output_file, format='png')
            print(f"   ✓ Created: {path}")
        except Exception as e:
            print(f"   ✗ Error visualizing {func_name}: {e}")
            print(f"     (Make sure graphviz is installed: apt-get install graphviz)")
    
    print("\n" + "=" * 60)
    print("Demo completed!")
    print("=" * 60)


def demo_voting():
    """Demo with Voting contract."""
    print("\n" + "=" * 60)
    print("Demo: Voting Contract")
    print("=" * 60)
    
    contract_path = 'examples/Voting.sol'
    
    if not os.path.exists(contract_path):
        print(f"Error: {contract_path} not found")
        return
    
    with open(contract_path, 'r') as f:
        source_code = f.read()
    
    parser = SolidityParser(source_code)
    parsed = parser.parse()
    
    print(f"\nFound {len(parsed['functions'])} function(s):")
    for func in parsed['functions']:
        print(f"  - {func['name']}")
    
    # Analyze specific function
    analyzer = CFGAnalyzer()
    
    # Find the vote function
    vote_func = next((f for f in parsed['functions'] if f['name'] == 'vote'), None)
    
    if vote_func:
        print(f"\nAnalyzing 'vote' function...")
        cfg = analyzer.analyze_function(vote_func['body'], vote_func['name'])
        print(f"  Nodes: {len(cfg['nodes'])}")
        print(f"  Edges: {len(cfg['edges'])}")
        
        visualizer = CFGVisualizer()
        os.makedirs('output', exist_ok=True)
        
        try:
            path = visualizer.visualize(cfg, 'output/cfg_vote', format='png')
            print(f"  ✓ Created: {path}")
        except Exception as e:
            print(f"  ✗ Error: {e}")


def print_stats():
    """Print statistics about the tool."""
    print("\n" + "=" * 60)
    print("CFG Visualizer Statistics")
    print("=" * 60)
    
    examples = ['SimpleToken.sol', 'Voting.sol', 'Auction.sol']
    total_contracts = 0
    total_functions = 0
    
    for example in examples:
        path = f'examples/{example}'
        if os.path.exists(path):
            with open(path, 'r') as f:
                source = f.read()
            
            parser = SolidityParser(source)
            parsed = parser.parse()
            
            total_contracts += len(parsed['contracts'])
            total_functions += len(parsed['functions'])
            
            print(f"\n{example}:")
            print(f"  Contracts: {len(parsed['contracts'])}")
            print(f"  Functions: {len(parsed['functions'])}")
    
    print(f"\nTotal:")
    print(f"  Contracts: {total_contracts}")
    print(f"  Functions: {total_functions}")


def main():
    """Main entry point."""
    print("\n")
    print("╔════════════════════════════════════════════════════════╗")
    print("║   Smart Contract CFG Visualizer - Demo Script         ║")
    print("║   Control Flow Graph Analysis Tool                    ║")
    print("╚════════════════════════════════════════════════════════╝")
    
    # Run demos
    demo_simple_token()
    demo_voting()
    print_stats()
    
    print("\n" + "=" * 60)
    print("To visualize other contracts, use:")
    print("  cfg-visualizer examples/SimpleToken.sol")
    print("  cfg-visualizer examples/Voting.sol --combined")
    print("  cfg-visualizer examples/Auction.sol -v")
    print("=" * 60 + "\n")


if __name__ == '__main__':
    main()
