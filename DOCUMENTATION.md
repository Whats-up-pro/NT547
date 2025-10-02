# Solidity CFG Visualizer - Technical Documentation

## Overview

This document explains the implementation details of the Solidity Control Flow Graph (CFG) Visualizer, focusing on the AST traversal and CFG construction logic.

## Architecture

The application consists of three main components:

1. **Code Editor** - Monaco Editor for Solidity code input with syntax highlighting
2. **CFG Builder** - Core logic for parsing AST and constructing CFG
3. **CFG Visualizer** - Interactive graph visualization using React Flow

## AST (Abstract Syntax Tree) Parsing

### Using @solidity-parser/parser

The application uses the `@solidity-parser/parser` library to convert Solidity source code into an Abstract Syntax Tree. The AST is a tree representation of the abstract syntactic structure of the source code.

```javascript
const ast = parser.parse(code, { 
  loc: true,      // Include location information
  range: true,    // Include range information
  tolerant: true  // Continue parsing even with errors
});
```

### AST Node Types

Key AST node types we process:

- `FunctionDefinition` - Function declarations
- `IfStatement` - Conditional branching
- `WhileStatement` - While loops
- `ForStatement` - For loops
- `DoWhileStatement` - Do-while loops
- `ReturnStatement` - Function returns
- `ExpressionStatement` - Expressions (including require/revert/assert)
- `VariableDeclarationStatement` - Variable declarations

## Control Flow Graph (CFG) Construction

### Basic Concepts

#### Basic Block
A **basic block** is a maximal sequence of consecutive statements with:
- **One entry point** - No jumps into the middle
- **One exit point** - No jumps out of the middle
- **Sequential execution** - All statements execute in order

#### Control Flow
**Control flow** represents the order in which statements are executed, including:
- Sequential flow (statement after statement)
- Conditional flow (if/else branches)
- Loop flow (while/for/do-while)
- Jump flow (return/revert/break/continue)

### CFG Building Algorithm

The CFG builder (`src/utils/cfgBuilder.js`) implements a recursive descent algorithm:

```
1. Create ENTRY block
2. Process function body statements recursively
3. Create EXIT block
4. Connect blocks with edges representing control flow
```

### Processing Different Statement Types

#### 1. Sequential Statements

Simple statements (assignments, declarations) are added to the current basic block:

```javascript
currentBlock.statements.push(statementToString(stmt));
```

#### 2. If Statements

If statements create a diamond-shaped control flow:

```
       [Condition]
          /    \
      [True]  [False]
          \    /
         [Merge]
```

Algorithm:
1. Create condition block with the boolean expression
2. Create true branch block
3. Process true branch statements recursively
4. Create false branch block (if else exists)
5. Process false branch statements recursively
6. Create merge block where both branches converge
7. Add edges: condition→true, condition→false, true→merge, false→merge

#### 3. While Loops

While loops create a cycle in the CFG:

```
    ↓
[Condition] ←─┐
    ↓         │
  [Body]  ────┘
    ↓
[After Loop]
```

Algorithm:
1. Create condition block
2. Create body block
3. Process body statements recursively
4. Add back-edge from body to condition (loop)
5. Create after-loop block
6. Add edges: current→condition, condition→body (true), body→condition (loop), condition→after (false)

#### 4. For Loops

For loops are similar to while loops but include initialization and increment:

```
[Init]
    ↓
[Condition] ←──┐
    ↓          │
  [Body]       │
    ↓          │
[Increment]────┘
    ↓
[After Loop]
```

Algorithm:
1. Add initialization to current block
2. Create condition block
3. Create body block
4. Process body statements recursively
5. Create increment block (if exists)
6. Add back-edge from increment to condition
7. Create after-loop block

#### 5. Do-While Loops

Do-while loops execute the body at least once:

```
    ↓
  [Body] ←─┐
    ↓      │
[Condition]─┘
    ↓
[After Loop]
```

#### 6. Return Statements

Return statements create a path directly to the exit:

```
[Statement]
    ↓
 [Return]
    ↓
  [EXIT]
```

#### 7. Require/Assert/Revert Statements

These create branching paths:

**Require/Assert:**
```
  [Check]
   /    \
[Pass] [EXIT]
  ↓
[Continue]
```

**Revert:**
```
[Revert]
    ↓
  [EXIT]
```

### Edge Types and Labels

Edges in the CFG are labeled to indicate the type of control flow:

- `normal` - Sequential flow
- `true` - Condition evaluated to true
- `false` - Condition evaluated to false
- `loop` - Back-edge in a loop
- `return` - Return statement
- `pass` - Require/assert check passed
- `fail` - Require/assert check failed
- `revert` - Explicit revert

## Visualization

### React Flow Integration

The CFG is visualized using React Flow, which provides:
- **Interactive graph rendering** - Pan, zoom, drag nodes
- **Minimap** - Overview of the entire graph
- **Controls** - Zoom in/out, fit view
- **Animations** - Animated edges for loops

### Node Styling

Different block types have distinct visual styles:

- **Entry blocks** - Green background (#90EE90)
- **Exit blocks** - Pink background (#FFB6C1)
- **Condition blocks** - Light blue (#87CEEB)
- **Loop blocks** - Plum (#DDA0DD)
- **Normal blocks** - White background

### Edge Styling

Edges are color-coded based on their type:

- **True branches** - Green (#22c55e)
- **False branches** - Red (#ef4444)
- **Loop edges** - Purple (#8b5cf6), dashed, animated
- **Return edges** - Orange (#f59e0b)
- **Fail/revert edges** - Dark red (#dc2626)

### Layout Algorithm

A simple hierarchical layout algorithm positions nodes:

1. **Level Assignment** - Use BFS to assign each node a level based on distance from entry
2. **Horizontal Positioning** - Distribute nodes at the same level horizontally
3. **Vertical Positioning** - Position levels vertically with fixed spacing

```javascript
node.position = {
  x: (index - (nodesInLevel.length - 1) / 2) * nodeWidth,
  y: level * levelHeight
};
```

## Interactive Features

### Click to Highlight

When a user clicks on a CFG node:

1. Extract the line numbers associated with that block
2. Pass the line numbers to the code editor
3. The editor highlights those lines and scrolls to show them

```javascript
const handleNodeClick = (block) => {
  const lines = [];
  for (let i = block.startLine; i <= block.endLine; i++) {
    lines.push(i);
  }
  onNodeClick(lines);
};
```

### Monaco Editor Decorations

The code editor uses Monaco's decoration API to highlight lines:

```javascript
const decorations = highlightedLines.map(lineNumber => ({
  range: {
    startLineNumber: lineNumber,
    startColumn: 1,
    endLineNumber: lineNumber,
    endColumn: 1
  },
  options: {
    isWholeLine: true,
    className: 'highlighted-line'
  }
}));
```

## Performance Considerations

### Parsing Performance

- AST parsing is typically fast (<100ms for typical contracts)
- Performance metrics are displayed to the user
- Parser runs in the main thread (consider Web Worker for very large contracts)

### CFG Construction Performance

- O(n) complexity where n is the number of statements
- Each statement is visited once during traversal
- Block creation and edge addition are O(1) operations

### Rendering Performance

- React Flow efficiently handles graphs with hundreds of nodes
- Virtual rendering for large graphs
- Minimap provides overview without rendering all details

## Testing Strategy

To test the CFG builder:

1. **Simple sequential code** - Verify basic blocks are created correctly
2. **If statements** - Check branching and merging
3. **Loops** - Verify back-edges and loop structure
4. **Nested structures** - Test if within while, etc.
5. **Require/revert** - Check special control flow handling
6. **Multiple functions** - Ensure isolation between functions

## Future Enhancements

Possible improvements:

1. **Path analysis** - Highlight feasible paths through the contract
2. **Dead code detection** - Identify unreachable blocks
3. **Complexity metrics** - Cyclomatic complexity calculation
4. **Export options** - Export CFG as image or GraphML
5. **Diff view** - Compare CFGs of different contract versions
6. **Data flow analysis** - Track variable definitions and uses
7. **Call graph** - Show function call relationships
8. **Symbolic execution** - Explore paths with symbolic values

## Limitations

Current limitations:

1. **Function calls** - External function calls are treated as simple statements
2. **Modifiers** - Function modifiers are not included in CFG
3. **Inline assembly** - Assembly blocks are treated as opaque statements
4. **Try/catch** - Exception handling not fully modeled
5. **Fallback/receive** - Special functions may need special handling

## References

- [Solidity Parser](https://github.com/solidity-parser/parser) - AST parser used
- [React Flow](https://reactflow.dev/) - Graph visualization library
- [Monaco Editor](https://microsoft.github.io/monaco-editor/) - Code editor
- [Control Flow Analysis](https://en.wikipedia.org/wiki/Control-flow_graph) - Theory behind CFG
