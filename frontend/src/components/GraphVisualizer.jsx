import React, { useCallback } from 'react';
import ReactFlow, {
  MiniMap,
  Controls,
  Background,
  useNodesState,
  useEdgesState,
} from 'reactflow';
import 'reactflow/dist/style.css';
import './GraphVisualizer.css';

// Custom node component
const CustomNode = ({ data }) => {
  const getNodeStyle = (type) => {
    switch (type) {
      case 'entry':
        return { backgroundColor: '#4ade80', color: '#000' };
      case 'exit':
        return { backgroundColor: '#f87171', color: '#fff' };
      case 'condition':
        return { backgroundColor: '#fbbf24', color: '#000', borderRadius: '50%' };
      case 'merge':
        return { backgroundColor: '#a78bfa', color: '#fff' };
      case 'return':
        return { backgroundColor: '#fb923c', color: '#fff' };
      default:
        return { backgroundColor: '#60a5fa', color: '#fff' };
    }
  };

  return (
    <div className="custom-node" style={getNodeStyle(data.type)}>
      <div className="node-label">{data.label}</div>
      {data.code && (
        <div className="node-code">{data.code}</div>
      )}
    </div>
  );
};

const nodeTypes = {
  custom: CustomNode,
};

const GraphVisualizer = ({ cfgData, onNodeClick }) => {
  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);

  React.useEffect(() => {
    if (cfgData && cfgData.nodes && cfgData.edges) {
      const flowNodes = cfgData.nodes.map(node => ({
        id: node.id,
        type: 'custom',
        data: {
          label: node.label,
          code: node.code,
          type: node.type,
          lineStart: node.lineStart,
          lineEnd: node.lineEnd,
        },
        position: node.position,
      }));

      const flowEdges = cfgData.edges.map(edge => ({
        id: edge.id,
        source: edge.source,
        target: edge.target,
        label: edge.label,
        type: 'smoothstep',
        animated: true,
        style: { stroke: '#888' },
        labelStyle: { fill: '#fff', fontSize: 12 },
        labelBgStyle: { fill: '#333' },
      }));

      setNodes(flowNodes);
      setEdges(flowEdges);
    }
  }, [cfgData, setNodes, setEdges]);

  const handleNodeClick = useCallback((event, node) => {
    if (onNodeClick && node.data.lineStart) {
      onNodeClick(node.data.lineStart, node.data.lineEnd);
    }
  }, [onNodeClick]);

  return (
    <div className="graph-visualizer-container">
      <div className="graph-header">
        <h3>Control Flow Graph</h3>
      </div>
      <div className="graph-content">
        {nodes.length > 0 ? (
          <ReactFlow
            nodes={nodes}
            edges={edges}
            onNodesChange={onNodesChange}
            onEdgesChange={onEdgesChange}
            onNodeClick={handleNodeClick}
            nodeTypes={nodeTypes}
            fitView
            attributionPosition="bottom-left"
          >
            <Controls />
            <MiniMap />
            <Background variant="dots" gap={12} size={1} />
          </ReactFlow>
        ) : (
          <div className="empty-state">
            <p>Enter Solidity code and click "Generate CFG" to visualize the control flow</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default GraphVisualizer;
