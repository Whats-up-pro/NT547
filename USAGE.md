# Usage Guide

## Command Line Interface

The CFG Visualizer provides a command-line interface for easy use.

### Basic Usage

```bash
cfg-visualizer <input_file> [options]
```

### Options

- `-o, --output`: Output file path (without extension)
- `-f, --format`: Output format (png, pdf, svg, dot)
- `--function`: Analyze specific function only
- `--combined`: Create combined visualization of all functions
- `--view`: Open the visualization after generation
- `-v, --verbose`: Verbose output

### Examples

#### Analyze a Contract

```bash
cfg-visualizer examples/SimpleToken.sol
```

This creates individual CFG visualizations for each function in the contract.

#### Specify Output Path and Format

```bash
cfg-visualizer examples/SimpleToken.sol -o output/mytoken -f pdf
```

Creates PDF files in the output directory.

#### Analyze Specific Function

```bash
cfg-visualizer examples/SimpleToken.sol --function transfer
```

Only analyzes and visualizes the `transfer` function.

#### Combined Visualization

```bash
cfg-visualizer examples/Voting.sol --combined
```

Creates a single visualization with all functions as subgraphs.

#### Verbose Mode

```bash
cfg-visualizer examples/Auction.sol -v
```

Prints detailed information about the analysis process.

## Python API

You can also use the tool programmatically in Python.

### Basic Example

```python
from cfg_visualizer import SolidityParser, CFGAnalyzer, CFGVisualizer

# Read source code
with open('contract.sol', 'r') as f:
    source_code = f.read()

# Parse
parser = SolidityParser(source_code)
parsed_data = parser.parse()

# Analyze
analyzer = CFGAnalyzer()
cfg_data = analyzer.analyze_function(
    parsed_data['functions'][0]['body'],
    parsed_data['functions'][0]['name']
)

# Visualize
visualizer = CFGVisualizer()
visualizer.visualize(cfg_data, 'output/cfg', format='png')
```

### Analyzing Multiple Functions

```python
from cfg_visualizer import SolidityParser, CFGAnalyzer, CFGVisualizer

# Parse contract
parser = SolidityParser(source_code)
parsed = parser.parse()

# Analyze all functions
analyzer = CFGAnalyzer()
cfg_list = []

for func in parsed['functions']:
    cfg = analyzer.analyze_function(func['body'], func['name'])
    cfg_list.append(cfg)

# Create visualizations
visualizer = CFGVisualizer()
visualizer.visualize_multiple(cfg_list, output_dir='output')
```

### Combined Visualization

```python
visualizer = CFGVisualizer()
visualizer.create_combined_visualization(
    cfg_list,
    output_file='combined_cfg',
    format='pdf'
)
```

## Output Formats

### PNG (Default)
Good for viewing and sharing. Suitable for documentation.

```bash
cfg-visualizer contract.sol -f png
```

### PDF
High-quality output suitable for reports and papers.

```bash
cfg-visualizer contract.sol -f pdf
```

### SVG
Vector format, scalable without quality loss.

```bash
cfg-visualizer contract.sol -f svg
```

### DOT
Graphviz source format, can be edited manually.

```bash
cfg-visualizer contract.sol -f dot
```

## Understanding the Output

### Node Types

- **Green Ellipse**: Entry point of function
- **Red Ellipse**: Exit point of function
- **Yellow Diamond**: Conditional statement (if)
- **Blue Diamond**: Loop statement (while, for)
- **Gray Rounded Box**: Return statement
- **White Rounded Box**: Regular statement

### Edge Types

- **Green Edge (true)**: True branch of conditional
- **Red Edge (false)**: False branch of conditional
- **Blue Dashed Edge (back)**: Loop back edge
- **Black Edge**: Sequential flow

## Tips

1. Use `--verbose` to debug issues
2. Use `--combined` for overview of entire contract
3. Use specific `--function` to focus on complex functions
4. PDF format is best for printing
5. SVG format is best for web embedding
