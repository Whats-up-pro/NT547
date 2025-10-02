"""
Command Line Interface for CFG Visualizer
"""

import argparse
import sys
import os
from pathlib import Path

from .parser import SolidityParser
from .analyzer import CFGAnalyzer
from .visualizer import CFGVisualizer


def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description='Control Flow Graph (CFG) Visualizer for Smart Contracts',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  cfg-visualizer contract.sol
  cfg-visualizer contract.sol -o output/cfg -f pdf
  cfg-visualizer contract.sol --function transfer
        """
    )
    
    parser.add_argument(
        'input_file',
        help='Path to Solidity smart contract file'
    )
    
    parser.add_argument(
        '-o', '--output',
        default='output/cfg',
        help='Output file path (without extension, default: output/cfg)'
    )
    
    parser.add_argument(
        '-f', '--format',
        default='png',
        choices=['png', 'pdf', 'svg', 'dot'],
        help='Output format (default: png)'
    )
    
    parser.add_argument(
        '--function',
        help='Analyze specific function only'
    )
    
    parser.add_argument(
        '--combined',
        action='store_true',
        help='Create combined visualization of all functions'
    )
    
    parser.add_argument(
        '--view',
        action='store_true',
        help='Open the visualization after generation'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Verbose output'
    )
    
    args = parser.parse_args()
    
    # Check if input file exists
    if not os.path.exists(args.input_file):
        print(f"Error: Input file '{args.input_file}' not found", file=sys.stderr)
        return 1
    
    # Read the source code
    try:
        with open(args.input_file, 'r', encoding='utf-8') as f:
            source_code = f.read()
    except Exception as e:
        print(f"Error reading file: {e}", file=sys.stderr)
        return 1
    
    if args.verbose:
        print(f"Parsing {args.input_file}...")
    
    # Parse the contract
    parser_obj = SolidityParser(source_code)
    parsed_data = parser_obj.parse()
    
    if args.verbose:
        print(f"Found {len(parsed_data['contracts'])} contract(s)")
        print(f"Found {len(parsed_data['functions'])} function(s)")
    
    # Analyze functions
    analyzer = CFGAnalyzer()
    cfg_list = []
    
    functions = parsed_data['functions']
    
    # Filter by function name if specified
    if args.function:
        functions = [f for f in functions if f['name'] == args.function]
        if not functions:
            print(f"Error: Function '{args.function}' not found", file=sys.stderr)
            return 1
    
    for func in functions:
        if args.verbose:
            print(f"Analyzing function: {func['name']}")
        
        cfg_data = analyzer.analyze_function(func['body'], func['name'])
        cfg_list.append(cfg_data)
    
    # Create output directory if needed
    output_dir = os.path.dirname(args.output)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Visualize
    visualizer = CFGVisualizer()
    
    try:
        if args.combined and len(cfg_list) > 1:
            if args.verbose:
                print(f"Creating combined visualization...")
            output_path = visualizer.create_combined_visualization(
                cfg_list, args.output, args.format
            )
            print(f"Combined CFG saved to: {output_path}")
        else:
            if args.verbose:
                print(f"Creating individual visualizations...")
            
            for cfg_data in cfg_list:
                function_name = cfg_data['function_name']
                output_file = f"{args.output}_{function_name}"
                
                output_path = visualizer.visualize(
                    cfg_data, output_file, args.format, args.view
                )
                print(f"CFG for {function_name} saved to: {output_path}")
    
    except Exception as e:
        print(f"Error creating visualization: {e}", file=sys.stderr)
        return 1
    
    if args.verbose:
        print("Done!")
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
