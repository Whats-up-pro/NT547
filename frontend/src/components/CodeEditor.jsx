import React from 'react';
import Editor from '@monaco-editor/react';
import './CodeEditor.css';

const CodeEditor = ({ code, onChange, highlightedLines }) => {
  const editorRef = React.useRef(null);

  const handleEditorDidMount = (editor) => {
    editorRef.current = editor;
  };

  React.useEffect(() => {
    if (editorRef.current && highlightedLines) {
      const decorations = highlightedLines.map(line => ({
        range: new window.monaco.Range(line, 1, line, 1),
        options: {
          isWholeLine: true,
          className: 'highlighted-line',
          glyphMarginClassName: 'highlighted-line-glyph'
        }
      }));
      
      editorRef.current.deltaDecorations([], decorations);
    }
  }, [highlightedLines]);

  return (
    <div className="code-editor-container">
      <div className="editor-header">
        <h3>Solidity Code Editor</h3>
      </div>
      <Editor
        height="calc(100% - 40px)"
        defaultLanguage="sol"
        value={code}
        onChange={onChange}
        onMount={handleEditorDidMount}
        theme="vs-dark"
        options={{
          minimap: { enabled: false },
          fontSize: 14,
          lineNumbers: 'on',
          scrollBeyondLastLine: false,
          automaticLayout: true,
        }}
      />
    </div>
  );
};

export default CodeEditor;
