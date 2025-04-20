import React, { useEffect, useState } from 'react';
import cytoscape from 'cytoscape';

export default function CFGPage() {
  const [elements, setElements] = useState([]);

  useEffect(() => {
    fetch('/api/cfg', {
      method: 'POST',
      body: JSON.stringify({ code: sampleCode }),
      headers: { 'Content-Type': 'application/json' },
    })
    .then(res => res.json())
    .then(json => {
      const nodes = json.nodes.map((n: any) => ({ data: { id: n.id, label: n.id } }));
      const edges = json.links.map((l: any) => ({ data: { source: l.source, target: l.target } }));
      setElements([...nodes, ...edges]);
    });
  }, []);

  useEffect(() => {
    if (elements.length > 0) {
      cytoscape({
        container: document.getElementById('cy'),
        elements,
        style: [{ selector: 'node', style: { label: 'data(label)', 'background-color': '#3B82F6' } }],
        layout: { name: 'breadthfirst' },
      });
    }
  }, [elements]);

  return <div id="cy" style={{ width: '100%', height: '600px' }} />;
}
