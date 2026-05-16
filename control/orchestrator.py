import hashlib, time
from pathlib import Path
from .patterns import PatternSpec
from .registry import Registry
from .graph import PatternGraph

class Orchestrator:
    def __init__(self, root: Path | None = None):
        self.root = root or Path(__file__).resolve().parents[1]
        self.registry = Registry(self.root)
        self.graph = PatternGraph(self.root)

    def code_hash(self, text: str) -> str:
        return hashlib.sha256(text.encode()).hexdigest()

    def register(self, pattern_id: str, domain: str, function: str, runtime: str, code: str, parent_id=None, rules=None):
        spec = PatternSpec(pattern_id=pattern_id, parent_id=parent_id, domain=domain, function=function, runtime=runtime, code_hash=self.code_hash(code), rules=rules or {}, key_fingerprint=hashlib.sha256((pattern_id+runtime).encode()).hexdigest()[:16])
        self.registry.upsert(spec)
        self.graph.g.add_node(pattern_id)
        self.graph.save()
        return spec

    def heartbeat(self, pattern_id: str, peer: str | None = None):
        if peer: self.graph.touch_edge(peer, pattern_id, 1)
        specs = self.registry.load()
        for spec in specs:
            if spec.pattern_id == pattern_id:
                spec.fitness = min(1.0, spec.fitness + 0.1)
                self.registry.upsert(spec)
                return spec
        raise KeyError(pattern_id)

    def choose_runtime(self, domain: str):
        specs = [s for s in self.registry.load() if s.domain == domain]
        if not specs: return None
        return sorted(specs, key=lambda s: (-s.fitness, s.runtime))[0]

    def spawn_bridge_patterns(self):
        bridges = []
        for a, b, d in self.graph.bridge_candidates():
            pid = f"bridge-{a[:4]}-{b[:4]}-{int(time.time())}"
            spec = self.register(pid, "bridge", f"{a}->{b}", "python", f"bridge for {a} {b}", rules={"from": a, "to": b, "weight": d.get('weight', 0)})
            bridges.append(spec)
        return bridges
