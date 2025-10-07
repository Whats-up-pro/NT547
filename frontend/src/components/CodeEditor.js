
import React, { useState } from 'react';
import Editor from 'react-simple-code-editor';
import Prism from 'prismjs';
import 'prismjs/components/prism-solidity';
import 'prismjs/themes/prism.css';
import './CodeEditor.css';


function CodeEditor({ value, onChange, selectedNode }) {
  const [cursorPos, setCursorPos] = useState({ line: 1, col: 1 });

  // Highlight code with Prism and custom highlight for selected lines
  const highlight = (code) => {
    const html = Prism.highlight(code, Prism.languages.solidity, 'solidity');
    // Highlight selected lines if any
    if (selectedNode && selectedNode.startLine && selectedNode.endLine) {
      const lines = html.split('\n');
      for (let i = selectedNode.startLine - 1; i < selectedNode.endLine; i++) {
        if (lines[i] !== undefined) {
          lines[i] = `<span class=\"highlighted-line\">${lines[i]}</span>`;
        }
      }
      return lines.join('\n');
    }
    return html;
  };

  // Update cursor position for info
  const updateCursorFromEvent = (e) => {
    const pos = e.target.selectionStart || 0;
    const textUpToPos = e.target.value.slice(0, pos);
    const line = textUpToPos.split('\n').length; // 1-based
    const lastNewlineIndex = textUpToPos.lastIndexOf('\n');
    const col = pos - (lastNewlineIndex + 1) + 1; // 1-based
    setCursorPos({ line, col });
  };

  const handleChange = (e) => {
    onChange(e.target.value);
    updateCursorFromEvent(e);
  };

  return (
    <div className="code-editor">
      <Editor
        value={value}
        onValueChange={onChange}
        highlight={highlight}
        padding={16}
        textareaClassName="code-textarea"
        onClick={updateCursorFromEvent}
        onKeyUp={updateCursorFromEvent}
        onSelect={updateCursorFromEvent}
        style={{ 
          fontFamily: 'Consolas, Monaco, Courier New, monospace',
          fontSize: 14, minHeight:'100%',
          background: '#1e1e1e',
          color: '#d4d4d4',
          overflow: 'auto', }}
      />
      <div className="selected-info">
        <div>Current line:  {cursorPos.line}</div>
        {selectedNode && (
          <div>Selected: Lines {selectedNode.startLine} - {selectedNode.endLine}</div>
        )}
      </div>
    </div>
  );
}

export default CodeEditor;
