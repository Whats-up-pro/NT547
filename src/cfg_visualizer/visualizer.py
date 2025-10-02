"""
CFG Visualizer Module
Visualizes Control Flow Graphs using graphviz.
"""

from graphviz import Digraph
from typing import Dict, List, Tuple, Any, Optional
import os


class CFGVisualizer:
    """Visualizer for Control Flow Graphs."""
    
    def __init__(self):
        """Initialize the visualizer."""
        self.graph = None
        
    def visualize(self, cfg_data: Dict[str, Any], output_file: str = "cfg", 
                  format: str = "png", view: bool = False) -> str:
        """
        Visualize a Control Flow Graph.
        
        Args:
            cfg_data: CFG data from analyzer
            output_file: Output file name (without extension)
            format: Output format (png, pdf, svg, etc.)
            view: Whether to open the visualization
            
        Returns:
            Path to the generated file
        """
        function_name = cfg_data.get('function_name', 'unknown')
        nodes = cfg_data.get('nodes', {})
        edges = cfg_data.get('edges', [])
        
        # Create a new directed graph
        dot = Digraph(comment=f'CFG for {function_name}')
        dot.attr(rankdir='TB')
        dot.attr('node', shape='box', style='rounded')
        
        # Add nodes
        for node_id, node in nodes.items():
            self._add_node(dot, node_id, node)
        
        # Add edges
        for edge in edges:
            from_id, to_id, label = edge
            self._add_edge(dot, from_id, to_id, label)
        
        # Render the graph
        output_path = dot.render(output_file, format=format, cleanup=True, view=view)
        
        return output_path
    
    def _add_node(self, dot: Digraph, node_id: int, node: Any):
        """Add a node to the graph."""
        node_type = node.type if hasattr(node, 'type') else 'statement'
        content = node.content if hasattr(node, 'content') else str(node)
        
        # Customize node appearance based on type
        if node_type == 'entry':
            dot.node(str(node_id), content, shape='ellipse', style='filled', 
                    fillcolor='lightgreen')
        elif node_type == 'exit':
            dot.node(str(node_id), content, shape='ellipse', style='filled', 
                    fillcolor='lightcoral')
        elif node_type == 'condition':
            dot.node(str(node_id), content, shape='diamond', style='filled', 
                    fillcolor='lightyellow')
        elif node_type == 'loop':
            dot.node(str(node_id), content, shape='diamond', style='filled', 
                    fillcolor='lightblue')
        elif node_type == 'return':
            dot.node(str(node_id), content, shape='box', style='filled,rounded', 
                    fillcolor='lightgray')
        else:
            dot.node(str(node_id), content, shape='box', style='rounded')
    
    def _add_edge(self, dot: Digraph, from_id: int, to_id: int, label: str = ""):
        """Add an edge to the graph."""
        if label:
            # Color edges based on label
            if label == 'true':
                dot.edge(str(from_id), str(to_id), label=label, color='green')
            elif label == 'false':
                dot.edge(str(from_id), str(to_id), label=label, color='red')
            elif label == 'back':
                dot.edge(str(from_id), str(to_id), label=label, color='blue', 
                        style='dashed')
            else:
                dot.edge(str(from_id), str(to_id), label=label)
        else:
            dot.edge(str(from_id), str(to_id))
    
    def visualize_multiple(self, cfg_list: List[Dict[str, Any]], 
                          output_dir: str = "output", format: str = "png") -> List[str]:
        """
        Visualize multiple Control Flow Graphs.
        
        Args:
            cfg_list: List of CFG data from analyzer
            output_dir: Output directory
            format: Output format
            
        Returns:
            List of paths to generated files
        """
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        output_files = []
        
        for i, cfg_data in enumerate(cfg_list):
            function_name = cfg_data.get('function_name', f'function_{i}')
            output_file = os.path.join(output_dir, f'cfg_{function_name}')
            
            try:
                output_path = self.visualize(cfg_data, output_file, format=format)
                output_files.append(output_path)
            except Exception as e:
                print(f"Error visualizing {function_name}: {e}")
        
        return output_files
    
    def create_combined_visualization(self, cfg_list: List[Dict[str, Any]], 
                                     output_file: str = "combined_cfg",
                                     format: str = "png") -> str:
        """
        Create a combined visualization of multiple CFGs.
        
        Args:
            cfg_list: List of CFG data from analyzer
            output_file: Output file name
            format: Output format
            
        Returns:
            Path to the generated file
        """
        dot = Digraph(comment='Combined CFGs')
        dot.attr(rankdir='TB')
        
        for i, cfg_data in enumerate(cfg_list):
            function_name = cfg_data.get('function_name', f'function_{i}')
            
            # Create a subgraph for each function
            with dot.subgraph(name=f'cluster_{i}') as sub:
                sub.attr(label=f'Function: {function_name}')
                sub.attr(style='rounded')
                sub.attr(color='blue')
                
                nodes = cfg_data.get('nodes', {})
                edges = cfg_data.get('edges', [])
                
                # Add nodes with prefix to avoid conflicts
                for node_id, node in nodes.items():
                    prefixed_id = f"{i}_{node_id}"
                    self._add_node_to_subgraph(sub, prefixed_id, node)
                
                # Add edges with prefixed IDs
                for edge in edges:
                    from_id, to_id, label = edge
                    prefixed_from = f"{i}_{from_id}"
                    prefixed_to = f"{i}_{to_id}"
                    self._add_edge(sub, prefixed_from, prefixed_to, label)
        
        # Render the combined graph
        output_path = dot.render(output_file, format=format, cleanup=True)
        
        return output_path
    
    def _add_node_to_subgraph(self, subgraph, node_id: str, node: Any):
        """Add a node to a subgraph."""
        node_type = node.type if hasattr(node, 'type') else 'statement'
        content = node.content if hasattr(node, 'content') else str(node)
        
        # Customize node appearance based on type
        if node_type == 'entry':
            subgraph.node(node_id, content, shape='ellipse', style='filled', 
                         fillcolor='lightgreen')
        elif node_type == 'exit':
            subgraph.node(node_id, content, shape='ellipse', style='filled', 
                         fillcolor='lightcoral')
        elif node_type == 'condition':
            subgraph.node(node_id, content, shape='diamond', style='filled', 
                         fillcolor='lightyellow')
        elif node_type == 'loop':
            subgraph.node(node_id, content, shape='diamond', style='filled', 
                         fillcolor='lightblue')
        elif node_type == 'return':
            subgraph.node(node_id, content, shape='box', style='filled,rounded', 
                         fillcolor='lightgray')
        else:
            subgraph.node(node_id, content, shape='box', style='rounded')
