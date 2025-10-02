# NT547 - Solidity CFG Visualizer
D02: Công cụ Trực quan hóa Đồ thị Luồng Điều khiển (CFG) cho Hợp đồng Thông minh

## Overview

A web-based tool for visualizing Control Flow Graphs (CFG) of Solidity smart contracts. This tool helps security analysts and developers understand the execution logic of smart contracts through interactive graph visualization.

## Features

✅ **Code Editor**: Monaco-based editor with Solidity syntax highlighting  
✅ **AST Parsing**: Using @solidity-parser/parser to convert Solidity to Abstract Syntax Tree  
✅ **CFG Generation**: Automatic control flow graph construction from AST  
✅ **Interactive Visualization**: React Flow-based graph with zoom, pan, and navigation  
✅ **Code Highlighting**: Click on nodes to highlight corresponding code lines  
✅ **Real-time Analysis**: Generate CFG instantly from code changes  

## Project Structure

```
NT547/
├── backend/              # Python Flask backend
│   ├── app.py           # Flask API server
│   ├── requirements.txt # Python dependencies
│   └── README.md        # Backend documentation
├── frontend/            # React frontend
│   ├── src/
│   │   ├── components/  # React components
│   │   │   ├── CodeEditor.jsx
│   │   │   └── GraphVisualizer.jsx
│   │   ├── utils/       # Utility functions
│   │   │   └── cfgBuilder.js
│   │   ├── App.jsx      # Main application
│   │   └── main.jsx     # Entry point
│   ├── package.json     # Frontend dependencies
│   └── README.md        # Frontend documentation
└── README.md            # This file
```

## Quick Start

### Prerequisites

- **Node.js** 16+ and npm
- **Python** 3.8+
- Windows, macOS, or Linux

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/Whats-up-pro/NT547.git
cd NT547
```

2. **Setup Backend**
```bash
cd backend
pip install -r requirements.txt
python app.py
```

The backend will run on `http://localhost:5000`

3. **Setup Frontend** (in a new terminal)
```bash
cd frontend
npm install
npm run dev
```

The frontend will run on `http://localhost:3000`

4. **Open your browser**

Navigate to `http://localhost:3000` to use the application.

## Usage

1. **Enter Solidity Code**: Paste or type your Solidity smart contract code in the editor
2. **Generate CFG**: Click the "Generate CFG" button
3. **Explore the Graph**: 
   - Pan by dragging the background
   - Zoom with mouse wheel or controls
   - Click nodes to highlight corresponding code lines
4. **Analyze**: Study the control flow paths, conditions, and loops

## Technology Stack

### Frontend
- **React 18**: UI framework
- **Vite**: Build tool and dev server
- **Monaco Editor**: Code editor (same as VS Code)
- **@solidity-parser/parser**: Solidity AST parsing
- **React Flow**: Graph visualization library

### Backend
- **Flask**: Python web framework
- **Flask-CORS**: Cross-origin resource sharing

## Node Types

The CFG uses different node types to represent different control structures:

- 🟢 **Entry**: Function entry point (green)
- 🔴 **Exit**: Function exit point (red)
- 🟡 **Condition**: Decision points (if/while/for) (yellow, circular)
- 🟣 **Merge**: Merge points after branches (purple)
- 🟠 **Return**: Return statements (orange)
- 🔵 **Statement**: Regular statements (blue)

## Supported Solidity Constructs

- ✅ Function definitions
- ✅ If/else statements
- ✅ While loops
- ✅ For loops
- ✅ Return statements
- ✅ Expression statements
- ✅ Binary operations
- ✅ Function calls

## Development

### Frontend Development
```bash
cd frontend
npm run dev    # Start dev server
npm run build  # Build for production
```

### Backend Development
```bash
cd backend
python app.py  # Start Flask server in debug mode
```

## Future Enhancements

- [ ] Support for require/assert/revert statements
- [ ] Function call graph visualization
- [ ] Export CFG as image/PDF
- [ ] Multiple contract analysis
- [ ] Integration with static analysis tools

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## License

MIT License

## Authors

NT547 Team - Ho Chi Minh City University of Technology