import React, { useState, useCallback } from 'react';
import CodeEditor from './components/CodeEditor';
import GraphVisualizer from './components/GraphVisualizer';
import { CFGBuilder } from './utils/cfgBuilder';
import './App.css';

const defaultCode = `// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract SimpleContract {
    uint256 public value;
    
    function setValue(uint256 newValue) public {
        if (newValue > 100) {
            value = 100;
        } else {
            value = newValue;
        }
    }
    
    function getValue() public view returns (uint256) {
        return value;
    }
    
    function complexLogic(uint256 x) public pure returns (uint256) {
        uint256 result = 0;
        
        for (uint256 i = 0; i < x; i++) {
            if (i % 2 == 0) {
                result += i;
            }
        }
        
        return result;
    }
}`;

function App() {
  const [code, setCode] = useState(defaultCode);
  const [cfgData, setCfgData] = useState(null);
  const [error, setError] = useState(null);
  const [highlightedLines, setHighlightedLines] = useState([]);
  const [isGenerating, setIsGenerating] = useState(false);

  const handleGenerateCFG = useCallback(() => {
    setIsGenerating(true);
    setError(null);
    
    try {
      const builder = new CFGBuilder();
      const cfg = builder.buildCFG(code);
      setCfgData(cfg);
      console.log('Generated CFG:', cfg);
    } catch (err) {
      setError(err.message);
      console.error('Error generating CFG:', err);
    } finally {
      setIsGenerating(false);
    }
  }, [code]);

  const handleNodeClick = useCallback((lineStart, lineEnd) => {
    if (lineStart && lineEnd) {
      const lines = [];
      for (let i = lineStart; i <= lineEnd; i++) {
        lines.push(i);
      }
      setHighlightedLines(lines);
    }
  }, []);

  const handleCodeChange = useCallback((newCode) => {
    setCode(newCode);
    setHighlightedLines([]);
  }, []);

  return (
    <div className="app">
      <header className="app-header">
        <h1>🔍 Solidity CFG Visualizer</h1>
        <p>Control Flow Graph Analysis Tool for Smart Contracts</p>
      </header>
      
      <div className="toolbar">
        <button 
          className="generate-btn"
          onClick={handleGenerateCFG}
          disabled={isGenerating}
        >
          {isGenerating ? '⏳ Generating...' : '🚀 Generate CFG'}
        </button>
        
        {error && (
          <div className="error-message">
            ⚠️ Error: {error}
          </div>
        )}
        
        {cfgData && cfgData.nodes && (
          <div className="info-message">
            ✅ Generated {cfgData.nodes.length} nodes and {cfgData.edges.length} edges
          </div>
        )}
      </div>

      <div className="content">
        <div className="panel editor-panel">
          <CodeEditor 
            code={code}
            onChange={handleCodeChange}
            highlightedLines={highlightedLines}
          />
        </div>
        
        <div className="panel graph-panel">
          <GraphVisualizer 
            cfgData={cfgData}
            onNodeClick={handleNodeClick}
          />
        </div>
      </div>

      <footer className="app-footer">
        <p>💡 Click on a node in the graph to highlight corresponding code lines</p>
      </footer>
    </div>
  );
}

export default App;
