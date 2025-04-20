import React, { useEffect, useState } from 'react';
import cytoscape from 'cytoscape';

export default function CFGPage() {
  const [elements, setElements] = useState([]);

  // Sample code or input code to send to backend for CFG generation
  const sampleCode = `function foo() { var x = 10; return x; }`;

  useEffect(() => {
    fetch('/api/cfg', {
      method: 'POST',
      body: JSON.stringify({ code: sampleCode }), // Send code to backend
      headers: { 'Content-Type': 'application/json' },
    })
    .then(res => res.json())
    .then(json => {
      // Map the nodes, adding taint info to the node's data
      const nodes = json.nodes.map((n: any) => ({
        data: { 
          id: n.id, 
          label: n.id, 
          taint: n.taint // Assuming taint data is present from backend
        }
      }));
      const edges = json.links.map((l: any) => ({
        data: { source: l.source, target: l.target }
      }));

      setElements([...nodes, ...edges]);
    });
  }, []);

  useEffect(() => {
    if (elements.length > 0) {
      cytoscape({
        container: document.getElementById('cy'),
        elements,
        style: [
          {
            selector: 'node',
            style: {
              label: 'data(label)',
              'background-color': '#3B82F6', // Default blue for nodes
            }
          },
          {
            selector: 'node[taint="source"]',  // Source nodes highlighted in yellow
            style: {
              'background-color': '#FACC15',  // Yellow for source
            }
          },
          {
            selector: 'node[taint="sink"]',  // Sink nodes highlighted in red
            style: {
              'background-color': '#EF4444',  // Red for sink
            }
          },
          {
            selector: 'edge',
            style: {
              width: 3,
              lineColor: '#ccc',
              targetArrowColor: '#ccc',
              targetArrowShape: 'triangle',
            }
          },
        ],
        layout: { name: 'breadthfirst' },
      });
    }
  }, [elements]);

  return <div id="cy" style={{ width: '100%', height: '600px' }} />;
}
