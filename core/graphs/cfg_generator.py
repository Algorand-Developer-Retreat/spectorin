import networkx as nx
import json

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
    return json.dumps(nx.readwrite.json_graph.node_link_data(G))
