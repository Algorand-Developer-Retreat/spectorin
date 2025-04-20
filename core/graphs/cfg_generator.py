import networkx as nx
import json
from core.analysis.taint_tracker import mark_taint_paths

def build_cfg_from_ast(ast):
    G = nx.DiGraph()

    def walk(node, parent=None):
        label = f"{node.type} ({node.start_point[0]})"
        G.add_node(label)

        if parent:
            G.add_edge(parent, label)

        for child in node.children:
            walk(child, label)

    walk(ast)
    return G

def export_cfg_json(G):
    taint_paths = mark_taint_paths(G)
    data = nx.readwrite.json_graph.node_link_data(G)

    for node in data["nodes"]:
        node_id = node["id"]
        node["taint"] = G.nodes[node_id].get("taint")

    data["taint_paths"] = taint_paths
    return json.dumps(data)
