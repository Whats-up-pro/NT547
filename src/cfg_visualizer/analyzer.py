"""
CFG Analyzer Module
Analyzes parsed smart contract code and builds Control Flow Graph.
"""

import re
from typing import Dict, List, Set, Tuple, Optional, Any
import networkx as nx


class CFGNode:
    """Represents a node in the Control Flow Graph."""
    
    def __init__(self, node_id: int, node_type: str, content: str = ""):
        """
        Initialize a CFG node.
        
        Args:
            node_id: Unique identifier for the node
            node_type: Type of node (entry, exit, statement, condition, etc.)
            content: Content/code of the node
        """
        self.id = node_id
        self.type = node_type
        self.content = content
        self.successors = []
        self.predecessors = []
    
    def __repr__(self):
        return f"CFGNode(id={self.id}, type={self.type})"


class CFGAnalyzer:
    """Analyzer for building Control Flow Graphs from smart contracts."""
    
    def __init__(self):
        """Initialize the CFG analyzer."""
        self.node_counter = 0
        self.nodes = {}
        self.edges = []
        self.graph = nx.DiGraph()
        
    def analyze_function(self, function_body: str, function_name: str = "") -> Dict[str, Any]:
        """
        Analyze a function and build its Control Flow Graph.
        
        Args:
            function_body: Function body code
            function_name: Name of the function
            
        Returns:
            Dictionary containing CFG information
        """
        self.node_counter = 0
        self.nodes = {}
        self.edges = []
        self.graph = nx.DiGraph()
        
        # Create entry node
        entry_node = self._create_node("entry", f"Entry: {function_name}")
        
        # Parse function body into statements
        statements = self._parse_statements(function_body)
        
        # Build CFG from statements
        exit_node = self._build_cfg_from_statements(statements, entry_node)
        
        # Create exit node if not created
        if exit_node is None:
            exit_node = self._create_node("exit", f"Exit: {function_name}")
        
        return {
            'function_name': function_name,
            'nodes': self.nodes,
            'edges': self.edges,
            'graph': self.graph,
            'entry': entry_node.id,
            'exit': exit_node.id if exit_node else None
        }
    
    def _create_node(self, node_type: str, content: str = "") -> CFGNode:
        """Create a new CFG node."""
        node = CFGNode(self.node_counter, node_type, content)
        self.nodes[self.node_counter] = node
        self.graph.add_node(self.node_counter, label=content, type=node_type)
        self.node_counter += 1
        return node
    
    def _add_edge(self, from_node: CFGNode, to_node: CFGNode, label: str = ""):
        """Add an edge between two nodes."""
        from_node.successors.append(to_node.id)
        to_node.predecessors.append(from_node.id)
        self.edges.append((from_node.id, to_node.id, label))
        self.graph.add_edge(from_node.id, to_node.id, label=label)
    
    def _parse_statements(self, code: str) -> List[Dict[str, Any]]:
        """Parse code into a list of statements."""
        statements = []
        
        # Remove function signature
        code = re.sub(r'function\s+\w+\s*\([^)]*\)[^{]*\{', '', code, 1)
        code = code.rstrip('}').strip()
        
        # Split by semicolons and braces
        lines = []
        current_line = ""
        brace_level = 0
        
        for char in code:
            current_line += char
            if char == '{':
                brace_level += 1
            elif char == '}':
                brace_level -= 1
                if brace_level == 0:
                    lines.append(current_line.strip())
                    current_line = ""
            elif char == ';' and brace_level == 0:
                lines.append(current_line.strip())
                current_line = ""
        
        if current_line.strip():
            lines.append(current_line.strip())
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            stmt = self._classify_statement(line)
            if stmt:
                statements.append(stmt)
        
        return statements
    
    def _classify_statement(self, line: str) -> Optional[Dict[str, Any]]:
        """Classify a statement by its type."""
        line = line.strip()
        
        if not line:
            return None
        
        # Check for if statement
        if line.startswith('if'):
            condition_match = re.match(r'if\s*\(([^)]+)\)', line)
            if condition_match:
                return {
                    'type': 'if',
                    'condition': condition_match.group(1),
                    'body': line,
                    'full': line
                }
        
        # Check for while loop
        if line.startswith('while'):
            condition_match = re.match(r'while\s*\(([^)]+)\)', line)
            if condition_match:
                return {
                    'type': 'while',
                    'condition': condition_match.group(1),
                    'body': line,
                    'full': line
                }
        
        # Check for for loop
        if line.startswith('for'):
            return {
                'type': 'for',
                'body': line,
                'full': line
            }
        
        # Check for return statement
        if 'return' in line:
            return {
                'type': 'return',
                'body': line,
                'full': line
            }
        
        # Check for require/assert
        if line.startswith('require') or line.startswith('assert'):
            return {
                'type': 'assertion',
                'body': line,
                'full': line
            }
        
        # Default to simple statement
        return {
            'type': 'statement',
            'body': line,
            'full': line
        }
    
    def _build_cfg_from_statements(self, statements: List[Dict[str, Any]], 
                                   current_node: CFGNode) -> Optional[CFGNode]:
        """Build CFG from a list of statements."""
        if not statements:
            return current_node
        
        for stmt in statements:
            stmt_type = stmt['type']
            
            if stmt_type == 'if':
                # Create condition node
                condition_node = self._create_node('condition', f"if ({stmt['condition']})")
                self._add_edge(current_node, condition_node)
                
                # Create true branch
                true_node = self._create_node('statement', 'true branch')
                self._add_edge(condition_node, true_node, 'true')
                
                # Create false branch
                false_node = self._create_node('statement', 'false branch')
                self._add_edge(condition_node, false_node, 'false')
                
                # Create merge node
                merge_node = self._create_node('merge', 'merge')
                self._add_edge(true_node, merge_node)
                self._add_edge(false_node, merge_node)
                
                current_node = merge_node
                
            elif stmt_type == 'while' or stmt_type == 'for':
                # Create loop condition node
                loop_node = self._create_node('loop', f"{stmt_type} ({stmt.get('condition', 'loop')})")
                self._add_edge(current_node, loop_node)
                
                # Create loop body
                body_node = self._create_node('statement', 'loop body')
                self._add_edge(loop_node, body_node, 'true')
                self._add_edge(body_node, loop_node, 'back')
                
                # Create exit from loop
                exit_loop_node = self._create_node('statement', 'exit loop')
                self._add_edge(loop_node, exit_loop_node, 'false')
                
                current_node = exit_loop_node
                
            elif stmt_type == 'return':
                # Create return node
                return_node = self._create_node('return', stmt['body'])
                self._add_edge(current_node, return_node)
                
                # Create exit node
                exit_node = self._create_node('exit', 'Exit')
                self._add_edge(return_node, exit_node)
                return exit_node
                
            else:
                # Create simple statement node
                stmt_node = self._create_node('statement', stmt['body'])
                self._add_edge(current_node, stmt_node)
                current_node = stmt_node
        
        return current_node
    
    def get_graph(self) -> nx.DiGraph:
        """Get the NetworkX graph representation."""
        return self.graph
    
    def get_nodes(self) -> Dict[int, CFGNode]:
        """Get all nodes in the CFG."""
        return self.nodes
    
    def get_edges(self) -> List[Tuple[int, int, str]]:
        """Get all edges in the CFG."""
        return self.edges
