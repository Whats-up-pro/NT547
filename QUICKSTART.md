# Quick Start Guide

## Installation (5 minutes)

```bash
# 1. Install system dependencies
sudo apt-get install graphviz  # Ubuntu/Debian
# brew install graphviz        # macOS

# 2. Clone and install
git clone https://github.com/Whats-up-pro/NT547.git
cd NT547
pip install -r requirements.txt
pip install -e .
```

## Quick Test

```bash
# Run the demo
python demo.py

# Test CLI
cfg-visualizer examples/SimpleToken.sol
```

## Common Commands

```bash
# Analyze entire contract
cfg-visualizer contract.sol

# Analyze specific function
cfg-visualizer contract.sol --function transfer

# Generate PDF
cfg-visualizer contract.sol -f pdf

# Combined visualization
cfg-visualizer contract.sol --combined

# Verbose mode
cfg-visualizer contract.sol -v
```

## Quick Python Example

```python
from cfg_visualizer import SolidityParser, CFGAnalyzer, CFGVisualizer

# Read contract
with open('contract.sol') as f:
    code = f.read()

# Parse → Analyze → Visualize
parser = SolidityParser(code)
data = parser.parse()

analyzer = CFGAnalyzer()
cfg = analyzer.analyze_function(data['functions'][0]['body'], 
                                data['functions'][0]['name'])

visualizer = CFGVisualizer()
visualizer.visualize(cfg, 'output/cfg')
```

## Output Files

Generated files are saved in the `output/` directory:
- `cfg_<function>.png` - Individual function CFGs
- `combined_cfg.png` - All functions in one diagram

## Troubleshooting

### "graphviz not found"
Install system graphviz: `sudo apt-get install graphviz`

### "No module named cfg_visualizer"
Run: `pip install -e .` from project root

### "Permission denied"
Use virtual environment or `--user` flag with pip

## Next Steps

- Read [USAGE.md](USAGE.md) for detailed usage
- Check [examples/](examples/) for sample contracts
- See [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) for architecture

## Get Help

```bash
cfg-visualizer --help
python demo.py
```
