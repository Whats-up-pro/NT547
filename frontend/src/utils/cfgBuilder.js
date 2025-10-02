import * as parser from '@solidity-parser/parser';

/**
 * Build Control Flow Graph from Solidity AST
 */
export class CFGBuilder {
  constructor() {
    this.nodes = [];
    this.edges = [];
    this.nodeIdCounter = 0;
    this.currentFunction = null;
  }

  /**
   * Create a new CFG node
   */
  createNode(type, label, lineStart, lineEnd, code = '') {
    const node = {
      id: `node-${this.nodeIdCounter++}`,
      type,
      label,
      lineStart,
      lineEnd,
      code,
      position: { x: 0, y: 0 }
    };
    this.nodes.push(node);
    return node;
  }

  /**
   * Create an edge between two nodes
   */
  createEdge(fromId, toId, label = '') {
    this.edges.push({
      id: `edge-${fromId}-${toId}-${this.edges.length}`,
      source: fromId,
      target: toId,
      label
    });
  }

  /**
   * Parse Solidity code and build CFG
   */
  buildCFG(solidityCode) {
    this.nodes = [];
    this.edges = [];
    this.nodeIdCounter = 0;

    try {
      const ast = parser.parse(solidityCode, {
        loc: true,
        range: true,
        tolerant: true
      });

      this.traverseAST(ast);
      this.layoutNodes();

      return {
        nodes: this.nodes,
        edges: this.edges
      };
    } catch (error) {
      console.error('Parse error:', error);
      throw new Error(`Failed to parse Solidity code: ${error.message}`);
    }
  }

  /**
   * Traverse the AST and extract CFG
   */
  traverseAST(ast) {
    if (!ast || !ast.children) return;

    ast.children.forEach(child => {
      if (child.type === 'ContractDefinition') {
        this.processContract(child);
      }
    });
  }

  /**
   * Process a contract definition
   */
  processContract(contract) {
    contract.subNodes.forEach(node => {
      if (node.type === 'FunctionDefinition') {
        this.processFunction(node);
      }
    });
  }

  /**
   * Process a function definition
   */
  processFunction(funcNode) {
    this.currentFunction = funcNode.name || 'fallback';
    
    const entryNode = this.createNode(
      'entry',
      `Function: ${this.currentFunction}`,
      funcNode.loc?.start.line,
      funcNode.loc?.start.line,
      `function ${this.currentFunction}`
    );

    const exitNode = this.createNode(
      'exit',
      `Exit: ${this.currentFunction}`,
      funcNode.loc?.end.line,
      funcNode.loc?.end.line,
      ''
    );

    if (funcNode.body) {
      const bodyNodes = this.processBlock(funcNode.body);
      
      if (bodyNodes.length > 0) {
        this.createEdge(entryNode.id, bodyNodes[0].id);
        this.createEdge(bodyNodes[bodyNodes.length - 1].id, exitNode.id);
      } else {
        this.createEdge(entryNode.id, exitNode.id);
      }
    } else {
      this.createEdge(entryNode.id, exitNode.id);
    }
  }

  /**
   * Process a block statement
   */
  processBlock(block) {
    const nodes = [];
    
    if (!block.statements || block.statements.length === 0) {
      return nodes;
    }

    let prevNode = null;

    block.statements.forEach((stmt, index) => {
      const stmtNodes = this.processStatement(stmt);
      
      if (stmtNodes.length > 0) {
        if (prevNode) {
          this.createEdge(prevNode.id, stmtNodes[0].id);
        }
        
        nodes.push(...stmtNodes);
        prevNode = stmtNodes[stmtNodes.length - 1];
      }
    });

    return nodes;
  }

  /**
   * Process a statement
   */
  processStatement(stmt) {
    const nodes = [];

    switch (stmt.type) {
      case 'IfStatement':
        nodes.push(...this.processIfStatement(stmt));
        break;
      
      case 'WhileStatement':
        nodes.push(...this.processWhileStatement(stmt));
        break;
      
      case 'ForStatement':
        nodes.push(...this.processForStatement(stmt));
        break;
      
      case 'ReturnStatement':
        nodes.push(this.createNode(
          'return',
          'Return',
          stmt.loc?.start.line,
          stmt.loc?.end.line,
          'return'
        ));
        break;
      
      case 'ExpressionStatement':
        if (stmt.expression) {
          const label = this.getExpressionLabel(stmt.expression);
          nodes.push(this.createNode(
            'statement',
            label,
            stmt.loc?.start.line,
            stmt.loc?.end.line,
            label
          ));
        }
        break;
      
      default:
        // Generic statement node
        nodes.push(this.createNode(
          'statement',
          stmt.type,
          stmt.loc?.start.line,
          stmt.loc?.end.line,
          stmt.type
        ));
        break;
    }

    return nodes;
  }

  /**
   * Process if statement
   */
  processIfStatement(stmt) {
    const conditionLabel = this.getExpressionLabel(stmt.condition);
    const conditionNode = this.createNode(
      'condition',
      `If: ${conditionLabel}`,
      stmt.loc?.start.line,
      stmt.loc?.start.line,
      `if (${conditionLabel})`
    );

    const trueNodes = stmt.trueBody ? this.processBlock(stmt.trueBody) : [];
    const falseNodes = stmt.falseBody ? this.processBlock(stmt.falseBody) : [];

    const mergeNode = this.createNode(
      'merge',
      'Merge',
      stmt.loc?.end.line,
      stmt.loc?.end.line,
      ''
    );

    // Connect condition to branches
    if (trueNodes.length > 0) {
      this.createEdge(conditionNode.id, trueNodes[0].id, 'true');
      this.createEdge(trueNodes[trueNodes.length - 1].id, mergeNode.id);
    } else {
      this.createEdge(conditionNode.id, mergeNode.id, 'true');
    }

    if (falseNodes.length > 0) {
      this.createEdge(conditionNode.id, falseNodes[0].id, 'false');
      this.createEdge(falseNodes[falseNodes.length - 1].id, mergeNode.id);
    } else {
      this.createEdge(conditionNode.id, mergeNode.id, 'false');
    }

    return [conditionNode, ...trueNodes, ...falseNodes, mergeNode];
  }

  /**
   * Process while statement
   */
  processWhileStatement(stmt) {
    const conditionLabel = this.getExpressionLabel(stmt.condition);
    const conditionNode = this.createNode(
      'condition',
      `While: ${conditionLabel}`,
      stmt.loc?.start.line,
      stmt.loc?.start.line,
      `while (${conditionLabel})`
    );

    const bodyNodes = stmt.body ? this.processBlock(stmt.body) : [];

    const exitNode = this.createNode(
      'merge',
      'Loop Exit',
      stmt.loc?.end.line,
      stmt.loc?.end.line,
      ''
    );

    // Connect condition to body and exit
    if (bodyNodes.length > 0) {
      this.createEdge(conditionNode.id, bodyNodes[0].id, 'true');
      this.createEdge(bodyNodes[bodyNodes.length - 1].id, conditionNode.id);
    } else {
      this.createEdge(conditionNode.id, conditionNode.id, 'true');
    }
    
    this.createEdge(conditionNode.id, exitNode.id, 'false');

    return [conditionNode, ...bodyNodes, exitNode];
  }

  /**
   * Process for statement
   */
  processForStatement(stmt) {
    const initLabel = stmt.initExpression ? this.getExpressionLabel(stmt.initExpression) : 'init';
    const initNode = this.createNode(
      'statement',
      `Init: ${initLabel}`,
      stmt.loc?.start.line,
      stmt.loc?.start.line,
      initLabel
    );

    const conditionLabel = stmt.conditionExpression ? this.getExpressionLabel(stmt.conditionExpression) : 'condition';
    const conditionNode = this.createNode(
      'condition',
      `For: ${conditionLabel}`,
      stmt.loc?.start.line,
      stmt.loc?.start.line,
      `for (${conditionLabel})`
    );

    const bodyNodes = stmt.body ? this.processBlock(stmt.body) : [];

    const updateLabel = stmt.loopExpression ? this.getExpressionLabel(stmt.loopExpression) : 'update';
    const updateNode = this.createNode(
      'statement',
      `Update: ${updateLabel}`,
      stmt.loc?.end.line,
      stmt.loc?.end.line,
      updateLabel
    );

    const exitNode = this.createNode(
      'merge',
      'Loop Exit',
      stmt.loc?.end.line,
      stmt.loc?.end.line,
      ''
    );

    // Connect nodes
    this.createEdge(initNode.id, conditionNode.id);
    
    if (bodyNodes.length > 0) {
      this.createEdge(conditionNode.id, bodyNodes[0].id, 'true');
      this.createEdge(bodyNodes[bodyNodes.length - 1].id, updateNode.id);
    } else {
      this.createEdge(conditionNode.id, updateNode.id, 'true');
    }
    
    this.createEdge(updateNode.id, conditionNode.id);
    this.createEdge(conditionNode.id, exitNode.id, 'false');

    return [initNode, conditionNode, ...bodyNodes, updateNode, exitNode];
  }

  /**
   * Get a readable label from an expression
   */
  getExpressionLabel(expr) {
    if (!expr) return '';

    switch (expr.type) {
      case 'BinaryOperation':
        return `${this.getExpressionLabel(expr.left)} ${expr.operator} ${this.getExpressionLabel(expr.right)}`;
      
      case 'Identifier':
        return expr.name;
      
      case 'NumberLiteral':
        return expr.number;
      
      case 'BooleanLiteral':
        return expr.value.toString();
      
      case 'FunctionCall':
        if (expr.expression) {
          const funcName = this.getExpressionLabel(expr.expression);
          return `${funcName}()`;
        }
        return 'call()';
      
      case 'MemberAccess':
        return `${this.getExpressionLabel(expr.expression)}.${expr.memberName}`;
      
      default:
        return expr.type;
    }
  }

  /**
   * Layout nodes in a hierarchical structure
   */
  layoutNodes() {
    if (this.nodes.length === 0) return;

    const layers = this.assignLayers();
    const layerWidth = 250;
    const layerHeight = 100;

    layers.forEach((layer, layerIndex) => {
      layer.forEach((node, nodeIndex) => {
        node.position = {
          x: nodeIndex * layerWidth + 100,
          y: layerIndex * layerHeight + 50
        };
      });
    });
  }

  /**
   * Assign nodes to layers for layout
   */
  assignLayers() {
    const layers = [];
    const visited = new Set();
    const nodeMap = new Map(this.nodes.map(n => [n.id, n]));

    // Find entry nodes
    const entryNodes = this.nodes.filter(n => n.type === 'entry');
    
    if (entryNodes.length === 0) {
      // If no entry nodes, start with first node
      if (this.nodes.length > 0) {
        entryNodes.push(this.nodes[0]);
      }
    }

    const queue = entryNodes.map(n => ({ node: n, layer: 0 }));
    visited.add(entryNodes[0]?.id);

    while (queue.length > 0) {
      const { node, layer } = queue.shift();
      
      if (!layers[layer]) {
        layers[layer] = [];
      }
      
      layers[layer].push(node);

      // Find outgoing edges
      const outgoingEdges = this.edges.filter(e => e.source === node.id);
      
      outgoingEdges.forEach(edge => {
        if (!visited.has(edge.target)) {
          visited.add(edge.target);
          const targetNode = nodeMap.get(edge.target);
          if (targetNode) {
            queue.push({ node: targetNode, layer: layer + 1 });
          }
        }
      });
    }

    // Add unvisited nodes
    this.nodes.forEach(node => {
      if (!visited.has(node.id)) {
        if (!layers[0]) layers[0] = [];
        layers[0].push(node);
      }
    });

    return layers;
  }
}
