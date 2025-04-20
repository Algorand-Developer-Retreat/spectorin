import networkx as nx

TAINT_SOURCES = ["input", "msg.sender", "request.args"]
TAINT_SINKS = ["eval", "exec", "call", "os.system"]

def mark_taint_paths(cfg: nx.DiGraph):
    tainted_nodes = []

    for node in cfg.nodes:
        for src in TAINT_SOURCES:
            if src in node.lower():
                cfg.nodes[node]["taint"] = "source"
                tainted_nodes.append(node)

        for sink in TAINT_SINKS:
            if sink in node.lower():
                cfg.nodes[node]["taint"] = "sink"

    taint_paths = []
    for source in tainted_nodes:
        for node in cfg.nodes:
            if cfg.nodes.get(node, {}).get("taint") == "sink":
                if nx.has_path(cfg, source, node):
                    taint_paths.append(nx.shortest_path(cfg, source, node))

    return taint_paths
