import json
from pathlib import Path
import networkx as nx

class PatternGraph:
    def __init__(self, root: Path):
        self.path = root / "data" / "topology.json"
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self.path.write_text('{"nodes":[],"edges":[]}')
        self.g = nx.DiGraph()
        self.load()

    def load(self):
        data = json.loads(self.path.read_text())
        self.g.clear()
        self.g.add_nodes_from(data.get("nodes", []))
        self.g.add_edges_from([(e[0], e[1], e[2]) for e in data.get("edges", [])])

    def save(self):
        data = {"nodes": list(self.g.nodes), "edges": [(u, v, d) for u, v, d in self.g.edges(data=True)]}
        self.path.write_text(json.dumps(data, indent=2))

    def touch_edge(self, a: str, b: str, delta: int = 1):
        self.g.add_node(a); self.g.add_node(b)
        if self.g.has_edge(a, b):
            self.g[a][b]["weight"] = self.g[a][b].get("weight", 0) + delta
        else:
            self.g.add_edge(a, b, weight=delta)
        self.save()

    def bridge_candidates(self, threshold: int = 3):
        return [(u, v, d) for u, v, d in self.g.edges(data=True) if d.get("weight", 0) >= threshold]
