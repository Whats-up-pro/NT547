# Solidity CFG Visualizer - Setup Guide

## Overview

This guide will help you set up and run the Solidity Control Flow Graph (CFG) Visualizer on Windows, macOS, or Linux.

## Prerequisites

### Required Software

1. **Node.js** (version 16 or higher)
   - Download from: https://nodejs.org/
   - Verify installation: `node --version`

2. **Python** (version 3.8 or higher)
   - Windows: Download from https://www.python.org/downloads/
   - macOS: `brew install python3`
   - Linux: `sudo apt-get install python3 python3-pip`
   - Verify installation: `python --version` or `python3 --version`

3. **npm** (comes with Node.js)
   - Verify installation: `npm --version`

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/Whats-up-pro/NT547.git
cd NT547
```

### 2. Setup Backend

```bash
cd backend
pip install -r requirements.txt
```

Or on some systems:
```bash
pip3 install -r requirements.txt
```

### 3. Setup Frontend

```bash
cd ../frontend
npm install
```

This will install all necessary dependencies including:
- React 18
- Vite (build tool)
- @solidity-parser/parser
- React Flow
- and other required packages

## Running the Application

### Step 1: Start the Backend Server

Open a terminal/command prompt and run:

```bash
cd backend
python app.py
```

Or on some systems:
```bash
python3 app.py
```

The backend server will start on `http://localhost:5000`

You should see output like:
```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

### Step 2: Start the Frontend Development Server

Open a **new** terminal/command prompt (keep the backend running) and run:

```bash
cd frontend
npm run dev
```

The frontend will start on `http://localhost:3000`

You should see output like:
```
  VITE v5.4.20  ready in 220 ms

  ➜  Local:   http://localhost:3000/
```

### Step 3: Open in Browser

Open your web browser and navigate to:
```
http://localhost:3000
```

## Using the Application

1. **Enter Solidity Code**: The code editor on the left contains a sample smart contract. You can modify it or paste your own Solidity code.

2. **Generate CFG**: Click the "🚀 Generate CFG" button in the toolbar.

3. **View the Graph**: The Control Flow Graph will appear on the right side, showing:
   - 🟢 Entry nodes (function entry points)
   - 🔴 Exit nodes (function exits)
   - 🟡 Condition nodes (if/while/for statements)
   - 🔵 Statement nodes (regular code statements)
   - 🟣 Merge nodes (where control flow merges)
   - 🟠 Return nodes (return statements)

4. **Interactive Features**:
   - **Click on a node** to highlight the corresponding code lines in the editor
   - **Zoom**: Use mouse wheel or the zoom controls
   - **Pan**: Click and drag the background
   - **Mini-map**: Use the mini-map in the bottom-right for navigation

## Troubleshooting

### Backend Issues

**Problem**: `ModuleNotFoundError: No module named 'flask'`
- **Solution**: Make sure you installed the requirements: `pip install -r requirements.txt`

**Problem**: Port 5000 already in use
- **Solution**: Stop other applications using port 5000, or modify `backend/app.py` to use a different port

### Frontend Issues

**Problem**: `npm install` fails
- **Solution**: Clear npm cache: `npm cache clean --force` and try again

**Problem**: Port 3000 already in use
- **Solution**: Stop other applications using port 3000, or modify `frontend/vite.config.js` to use a different port

**Problem**: Build warnings about module externalization
- **Solution**: These are warnings from the Solidity parser for browser compatibility and can be safely ignored

### General Issues

**Problem**: Blank page or errors in browser console
- **Solution**: 
  1. Make sure both backend and frontend servers are running
  2. Check browser console (F12) for specific errors
  3. Try clearing browser cache and reloading

## Building for Production

### Build Frontend

```bash
cd frontend
npm run build
```

This creates optimized production files in `frontend/dist/`

### Preview Production Build

```bash
npm run preview
```

## Project Structure

```
NT547/
├── backend/              # Python Flask backend
│   ├── app.py           # Flask server
│   └── requirements.txt # Python dependencies
├── frontend/            # React frontend
│   ├── src/
│   │   ├── components/  # React components
│   │   ├── utils/       # CFG builder logic
│   │   ├── App.jsx      # Main app component
│   │   └── main.jsx     # Entry point
│   ├── package.json     # Node dependencies
│   └── vite.config.js   # Vite configuration
└── README.md            # Main documentation
```

## Features

✅ Solidity code editor with syntax highlighting  
✅ Automatic CFG generation from Solidity code  
✅ Interactive graph visualization  
✅ Code-to-graph linking (click nodes to highlight code)  
✅ Support for control structures (if/else, for, while)  
✅ Function-level CFG analysis  
✅ Zoom and pan controls  
✅ Mini-map navigation  

## Support

For issues or questions:
- Create an issue on GitHub: https://github.com/Whats-up-pro/NT547/issues
- Check existing documentation in the repository

## License

MIT License
