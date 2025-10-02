import React, { useState, useCallback } from 'react';
import CodeEditor from './components/CodeEditor';
import CFGVisualizer from './components/CFGVisualizer';
import { CFGBuilder, extractFunctionsFromAST } from './utils/cfgBuilder';
import parser from '@solidity-parser/parser';
import './App.css';

const defaultCode = `// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Example {
    uint256 public value;
    
    function setValue(uint256 _value) public {
        require(_value > 0, "Value must be positive");
        
        if (_value > 100) {
            value = 100;
        } else {
            value = _value;
        }
    }
    
    function processValue() public returns (uint256) {
        if (value == 0) {
            return 0;
        }
        
        uint256 result = 0;
        for (uint256 i = 0; i < value; i++) {
            result += i;
        }
        
        return result;
    }
    
    function checkAndReset() public {
        require(value > 0, "Value is already zero");
        
        while (value > 0) {
            value--;
            if (value == 50) {
                break;
            }
        }
    }
}`;

function App() {
  const [code, setCode] = useState(defaultCode);
  const [functions, setFunctions] = useState([]);
  const [selectedFunction, setSelectedFunction] = useState(null);
  const [cfg, setCfg] = useState(null);
  const [error, setError] = useState(null);
  const [highlightedLines, setHighlightedLines] = useState([]);
  const [parseStats, setParseStats] = useState(null);

  const parseCode = useCallback(() => {
    try {
      setError(null);
      setHighlightedLines([]);
      
      const startTime = performance.now();
      
      // Parse the Solidity code into AST
      const ast = parser.parse(code, { 
        loc: true, 
        range: true,
        tolerant: true 
      });
      
      // Extract functions from AST
      const extractedFunctions = extractFunctionsFromAST(ast);
      
      const parseTime = performance.now() - startTime;
      
      setFunctions(extractedFunctions);
      
      if (extractedFunctions.length > 0) {
        // Automatically select the first function
        const firstFunc = extractedFunctions[0];
        setSelectedFunction(firstFunc);
        
        // Build CFG for the first function
        const builder = new CFGBuilder();
        const funcCfg = builder.buildFunctionCFG(firstFunc.node);
        setCfg(funcCfg);
        
        setParseStats({
          functions: extractedFunctions.length,
          blocks: funcCfg.blocks.length,
          edges: funcCfg.edges.length,
          parseTime: parseTime.toFixed(2)
        });
      } else {
        setCfg(null);
        setParseStats(null);
        setError('No functions found in the contract.');
      }
    } catch (err) {
      console.error('Parse error:', err);
      setError(`Parse error: ${err.message}`);
      setFunctions([]);
      setCfg(null);
      setParseStats(null);
    }
  }, [code]);

  const handleFunctionSelect = useCallback((func) => {
    setSelectedFunction(func);
    setHighlightedLines([]);
    
    const builder = new CFGBuilder();
    const funcCfg = builder.buildFunctionCFG(func.node);
    setCfg(funcCfg);
    
    setParseStats(prev => ({
      ...prev,
      blocks: funcCfg.blocks.length,
      edges: funcCfg.edges.length
    }));
  }, []);

  const handleNodeClick = useCallback((lines) => {
    setHighlightedLines(lines);
  }, []);

  const handleCodeChange = useCallback((newCode) => {
    setCode(newCode);
  }, []);

  return (
    <div className="app">
      <header className="header">
        <div className="header-content">
          <h1>🔍 Solidity CFG Visualizer</h1>
          <p>Control Flow Graph visualization tool for Solidity smart contracts</p>
        </div>
        <button className="parse-button" onClick={parseCode}>
          Parse & Generate CFG
        </button>
      </header>

      <div className="main-container">
        <div className="left-panel">
          <div className="panel-header">
            <h3>Solidity Code</h3>
            {parseStats && (
              <span className="stats">
                ⚡ Parsed in {parseStats.parseTime}ms
              </span>
            )}
          </div>
          <div className="editor-container">
            <CodeEditor 
              value={code}
              onChange={handleCodeChange}
              highlightedLines={highlightedLines}
            />
          </div>
        </div>

        <div className="right-panel">
          <div className="panel-header">
            <h3>Control Flow Graph</h3>
            {parseStats && (
              <span className="stats">
                📊 {parseStats.blocks} blocks, {parseStats.edges} edges
              </span>
            )}
          </div>

          {error && (
            <div className="error-message">
              <strong>Error:</strong> {error}
            </div>
          )}

          {functions.length > 0 && (
            <div className="function-selector">
              <label>Select Function:</label>
              <select 
                value={selectedFunction?.name || ''} 
                onChange={(e) => {
                  const func = functions.find(f => f.name === e.target.value);
                  if (func) handleFunctionSelect(func);
                }}
              >
                {functions.map((func) => (
                  <option key={func.name} value={func.name}>
                    {func.name} ({func.visibility})
                  </option>
                ))}
              </select>
            </div>
          )}

          <div className="cfg-container">
            <CFGVisualizer cfg={cfg} onNodeClick={handleNodeClick} />
          </div>

          <div className="instructions">
            <p>💡 <strong>Tip:</strong> Click on CFG nodes to highlight corresponding code lines</p>
          </div>
        </div>
      </div>

      <div className="legend">
        <h4>Legend:</h4>
        <div className="legend-items">
          <div className="legend-item">
            <div className="legend-box entry"></div>
            <span>Entry Point</span>
          </div>
          <div className="legend-item">
            <div className="legend-box exit"></div>
            <span>Exit Point</span>
          </div>
          <div className="legend-item">
            <div className="legend-box condition"></div>
            <span>Condition</span>
          </div>
          <div className="legend-item">
            <div className="legend-box loop"></div>
            <span>Loop</span>
          </div>
          <div className="legend-item">
            <div className="legend-box normal"></div>
            <span>Normal Block</span>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
