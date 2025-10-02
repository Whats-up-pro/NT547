import React from 'react';
import './CodeEditor.css';

const CodeEditor = ({ code, onChange, highlightedLines }) => {
  const [lineNumbers, setLineNumbers] = React.useState([]);
  const textareaRef = React.useRef(null);

  React.useEffect(() => {
    if (code) {
      const lines = code.split('\n');
      setLineNumbers(lines.map((_, i) => i + 1));
    }
  }, [code]);

  const handleChange = (e) => {
    if (onChange) {
      onChange(e.target.value);
    }
  };

  const getLineClass = (lineNumber) => {
    if (highlightedLines && highlightedLines.includes(lineNumber)) {
      return 'line-number highlighted';
    }
    return 'line-number';
  };

  return (
    <div className="code-editor-container">
      <div className="editor-header">
        <h3>Solidity Code Editor</h3>
      </div>
      <div className="editor-content">
        <div className="line-numbers">
          {lineNumbers.map(num => (
            <div key={num} className={getLineClass(num)}>{num}</div>
          ))}
        </div>
        <textarea
          ref={textareaRef}
          className="code-textarea"
          value={code}
          onChange={handleChange}
          spellCheck={false}
          wrap="off"
        />
      </div>
    </div>
  );
};

export default CodeEditor;
