# Installation Guide

## System Requirements

- Python 3.8 or higher
- pip (Python package manager)
- Graphviz (system package)

## Step 1: Install Graphviz

### Ubuntu/Debian
```bash
sudo apt-get update
sudo apt-get install graphviz
```

### macOS
```bash
brew install graphviz
```

### Windows
1. Download installer from https://graphviz.org/download/
2. Run the installer
3. Add Graphviz to PATH

## Step 2: Clone Repository

```bash
git clone https://github.com/Whats-up-pro/NT547.git
cd NT547
```

## Step 3: Create Virtual Environment (Optional but Recommended)

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

## Step 4: Install Python Dependencies

```bash
pip install -r requirements.txt
```

## Step 5: Install the Package

```bash
pip install -e .
```

This installs the package in editable mode, so changes to the source code are immediately reflected.

## Step 6: Verify Installation

```bash
cfg-visualizer --help
```

You should see the help message for the tool.

## Step 7: Run Demo

```bash
python demo.py
```

This will analyze the example contracts and create visualizations in the `output/` directory.

## Troubleshooting

### "graphviz not found" error

Make sure Graphviz is installed on your system (not just the Python package). The Python `graphviz` package is a wrapper that requires the system Graphviz to be installed.

### Import errors

Make sure you're in the correct directory and have activated your virtual environment if you're using one.

### Permission errors

On Linux/macOS, you might need to use `sudo` for system-wide installation, or use a virtual environment for local installation.
