# Frontend Setup

## Requirements
- Node.js 16+ 
- npm or yarn

## Installation

1. Install dependencies:
```bash
npm install
```

## Running the Frontend

Development mode:
```bash
npm run dev
```

The frontend will run on `http://localhost:3000`

Build for production:
```bash
npm run build
```

Preview production build:
```bash
npm run preview
```

## Features

- **Code Editor**: Monaco Editor with Solidity syntax highlighting
- **CFG Generation**: Automatic control flow graph generation from Solidity code
- **Interactive Visualization**: Click on nodes to highlight corresponding code lines
- **Real-time Updates**: Edit code and regenerate CFG instantly

## Technologies Used

- React 18
- Vite (build tool)
- Monaco Editor (code editor)
- @solidity-parser/parser (Solidity AST parsing)
- React Flow (graph visualization)
