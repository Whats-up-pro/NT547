import React, { useCallback, useMemo } from 'react';
import ReactFlow, {
  MiniMap,
  Controls,
  Background,
  useNodesState,
  useEdgesState,
  MarkerType,
  Position,
} from 'reactflow';
import 'reactflow/dist/style.css';

const CFGVisualizer = ({ cfg, onNodeClick }) => {
  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);

  // Convert CFG blocks to React Flow nodes
  React.useEffect(() => {
    if (!cfg || !cfg.blocks) {
      setNodes([]);
      setEdges([]);
      return;
    }

    // Create nodes with hierarchical layout
    const newNodes = cfg.blocks.map((block, index) => {
      const isEntry = block.label.startsWith('Entry');
      const isExit = block.label === 'Exit';
      const isCondition = block.label.includes('Condition') || block.label.includes('If');
      const isLoop = block.label.includes('Loop') || block.label.includes('While') || block.label.includes('For');
      
      let nodeType = 'default';
      let style = {
        background: '#fff',
        border: '2px solid #1a192b',
        borderRadius: '8px',
        padding: '10px',
        fontSize: '12px',
        width: 180,
      };

      if (isEntry) {
        style.background = '#90EE90';
        style.border = '2px solid #228B22';
      } else if (isExit) {
        style.background = '#FFB6C1';
        style.border = '2px solid #DC143C';
      } else if (isCondition) {
        style.background = '#87CEEB';
        style.border = '2px solid #4682B4';
        style.borderRadius = '4px';
      } else if (isLoop) {
        style.background = '#DDA0DD';
        style.border = '2px solid #9370DB';
      }

      const statementsText = block.statements.length > 0 
        ? block.statements.slice(0, 3).join('\n') + (block.statements.length > 3 ? '\n...' : '')
        : '';

      return {
        id: block.id,
        data: {
          label: (
            <div onClick={() => handleNodeClick(block)} style={{ cursor: 'pointer' }}>
              <div style={{ fontWeight: 'bold', marginBottom: '5px', color: '#333' }}>
                {block.label}
              </div>
              {statementsText && (
                <div style={{ 
                  fontSize: '10px', 
                  color: '#666',
                  whiteSpace: 'pre-wrap',
                  maxHeight: '60px',
                  overflow: 'hidden',
                  textOverflow: 'ellipsis'
                }}>
                  {statementsText}
                </div>
              )}
              {block.startLine && (
                <div style={{ fontSize: '9px', color: '#999', marginTop: '3px' }}>
                  Lines: {block.startLine}-{block.endLine || block.startLine}
                </div>
              )}
            </div>
          ),
          block: block
        },
        position: { x: 0, y: 0 },
        style,
        sourcePosition: Position.Bottom,
        targetPosition: Position.Top,
      };
    });

    // Simple hierarchical layout
    const layoutNodes = calculateLayout(newNodes, cfg.edges);
    setNodes(layoutNodes);

    // Create edges
    const newEdges = cfg.edges.map((edge, index) => {
      let edgeStyle = {
        stroke: '#333',
        strokeWidth: 2,
      };
      let label = edge.label;

      // Color code edges based on type
      if (edge.label === 'true') {
        edgeStyle.stroke = '#22c55e';
        label = '✓ true';
      } else if (edge.label === 'false') {
        edgeStyle.stroke = '#ef4444';
        label = '✗ false';
      } else if (edge.label === 'loop') {
        edgeStyle.stroke = '#8b5cf6';
        edgeStyle.strokeDasharray = '5,5';
        label = '↻ loop';
      } else if (edge.label === 'return') {
        edgeStyle.stroke = '#f59e0b';
        label = '← return';
      } else if (edge.label === 'fail' || edge.label === 'revert') {
        edgeStyle.stroke = '#dc2626';
        label = '✗ ' + edge.label;
      } else if (edge.label === 'pass') {
        edgeStyle.stroke = '#10b981';
        label = '✓ pass';
      }

      return {
        id: `edge-${edge.from}-${edge.to}-${index}`,
        source: edge.from,
        target: edge.to,
        label,
        type: 'smoothstep',
        animated: edge.label === 'loop',
        style: edgeStyle,
        markerEnd: {
          type: MarkerType.ArrowClosed,
          color: edgeStyle.stroke,
        },
        labelStyle: { 
          fill: edgeStyle.stroke, 
          fontWeight: 600,
          fontSize: '11px'
        },
        labelBgStyle: { 
          fill: '#fff', 
          fillOpacity: 0.8 
        }
      };
    });

    setEdges(newEdges);
  }, [cfg]);

  const handleNodeClick = useCallback((block) => {
    if (onNodeClick && block.startLine) {
      const lines = [];
      for (let i = block.startLine; i <= (block.endLine || block.startLine); i++) {
        lines.push(i);
      }
      onNodeClick(lines);
    }
  }, [onNodeClick]);

  if (!cfg || !cfg.blocks || cfg.blocks.length === 0) {
    return (
      <div style={{ 
        width: '100%', 
        height: '100%', 
        display: 'flex', 
        alignItems: 'center', 
        justifyContent: 'center',
        color: '#666',
        fontSize: '16px'
      }}>
        No CFG to display. Parse Solidity code first.
      </div>
    );
  }

  return (
    <div style={{ width: '100%', height: '100%' }}>
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        fitView
        attributionPosition="bottom-left"
      >
        <Controls />
        <MiniMap 
          nodeColor={(node) => {
            if (node.style?.background) return node.style.background;
            return '#fff';
          }}
          nodeStrokeWidth={3}
          zoomable
          pannable
        />
        <Background variant="dots" gap={12} size={1} />
      </ReactFlow>
    </div>
  );
};

// Simple hierarchical layout algorithm
function calculateLayout(nodes, edges) {
  if (nodes.length === 0) return nodes;

  // Build adjacency list
  const adjacencyList = new Map();
  nodes.forEach(node => adjacencyList.set(node.id, []));
  edges.forEach(edge => {
    if (adjacencyList.has(edge.from)) {
      adjacencyList.get(edge.from).push(edge.to);
    }
  });

  // Calculate levels using BFS
  const levels = new Map();
  const queue = [nodes[0].id];
  levels.set(nodes[0].id, 0);

  while (queue.length > 0) {
    const nodeId = queue.shift();
    const currentLevel = levels.get(nodeId);

    const neighbors = adjacencyList.get(nodeId) || [];
    neighbors.forEach(neighbor => {
      if (!levels.has(neighbor)) {
        levels.set(neighbor, currentLevel + 1);
        queue.push(neighbor);
      }
    });
  }

  // Group nodes by level
  const levelGroups = new Map();
  nodes.forEach(node => {
    const level = levels.get(node.id) || 0;
    if (!levelGroups.has(level)) {
      levelGroups.set(level, []);
    }
    levelGroups.get(level).push(node);
  });

  // Position nodes
  const levelHeight = 150;
  const nodeWidth = 200;

  levelGroups.forEach((nodesInLevel, level) => {
    const totalWidth = nodesInLevel.length * nodeWidth;
    nodesInLevel.forEach((node, index) => {
      node.position = {
        x: (index - (nodesInLevel.length - 1) / 2) * nodeWidth,
        y: level * levelHeight
      };
    });
  });

  return nodes;
}

export default CFGVisualizer;
