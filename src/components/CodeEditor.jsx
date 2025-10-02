import React from 'react';
import Editor from '@monaco-editor/react';

const CodeEditor = ({ value, onChange, highlightedLines }) => {
  const editorRef = React.useRef(null);
  const decorationsRef = React.useRef([]);

  const handleEditorDidMount = (editor, monaco) => {
    editorRef.current = editor;
    
    // Configure Solidity language support
    if (!monaco.languages.getLanguages().some(lang => lang.id === 'solidity')) {
      monaco.languages.register({ id: 'solidity' });
      monaco.languages.setMonarchTokensProvider('solidity', {
        keywords: [
          'pragma', 'solidity', 'contract', 'interface', 'library', 'function', 
          'constructor', 'modifier', 'event', 'struct', 'enum', 'mapping',
          'public', 'private', 'internal', 'external', 'pure', 'view', 'payable',
          'memory', 'storage', 'calldata', 'if', 'else', 'for', 'while', 'do',
          'return', 'break', 'continue', 'require', 'assert', 'revert', 'emit',
          'new', 'delete', 'this', 'super', 'true', 'false', 'address', 'uint',
          'int', 'bool', 'string', 'bytes', 'byte'
        ],
        tokenizer: {
          root: [
            [/[a-z_$][\w$]*/, {
              cases: {
                '@keywords': 'keyword',
                '@default': 'identifier'
              }
            }],
            [/[A-Z][\w\$]*/, 'type.identifier'],
            [/".*?"/, 'string'],
            [/'.*?'/, 'string'],
            [/\d+/, 'number'],
            [/\/\/.*$/, 'comment'],
            [/\/\*/, 'comment', '@comment'],
          ],
          comment: [
            [/[^\/*]+/, 'comment'],
            [/\*\//, 'comment', '@pop'],
            [/[\/*]/, 'comment']
          ]
        }
      });
    }
  };

  React.useEffect(() => {
    if (editorRef.current && highlightedLines && highlightedLines.length > 0) {
      const editor = editorRef.current;
      
      // Remove previous decorations
      decorationsRef.current = editor.deltaDecorations(decorationsRef.current, []);
      
      // Add new decorations for highlighted lines
      const newDecorations = highlightedLines.map(lineNumber => ({
        range: {
          startLineNumber: lineNumber,
          startColumn: 1,
          endLineNumber: lineNumber,
          endColumn: 1
        },
        options: {
          isWholeLine: true,
          className: 'highlighted-line',
          glyphMarginClassName: 'highlighted-line-glyph'
        }
      }));
      
      decorationsRef.current = editor.deltaDecorations([], newDecorations);
      
      // Scroll to the first highlighted line
      if (highlightedLines.length > 0) {
        editor.revealLineInCenter(highlightedLines[0]);
      }
    }
  }, [highlightedLines]);

  return (
    <div style={{ height: '100%', width: '100%' }}>
      <Editor
        height="100%"
        defaultLanguage="solidity"
        value={value}
        onChange={onChange}
        onMount={handleEditorDidMount}
        theme="vs-dark"
        options={{
          minimap: { enabled: true },
          fontSize: 14,
          lineNumbers: 'on',
          rulers: [],
          scrollBeyondLastLine: false,
          automaticLayout: true,
          wordWrap: 'on'
        }}
      />
      <style>{`
        .highlighted-line {
          background-color: rgba(255, 200, 0, 0.3);
        }
        .highlighted-line-glyph {
          background-color: rgba(255, 200, 0, 0.8);
          width: 5px !important;
          margin-left: 3px;
        }
      `}</style>
    </div>
  );
};

export default CodeEditor;
