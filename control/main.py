from pathlib import Path
from .orchestrator import Orchestrator
from .patterns import PatternSpec

def main():
    root = Path(__file__).resolve().parents[1]
    o = Orchestrator(root)
    code_a = "dispatch-core"
    code_b = "parser-core"
    a = o.register("root-001", "router", "dispatch", "python", code_a)
    b = o.register("parser-001", "parser", "extract", "rust", code_b, parent_id=a.pattern_id)
    o.heartbeat(a.pattern_id)
    o.heartbeat(b.pattern_id, peer=a.pattern_id)
    bridges = o.spawn_bridge_patterns()
    print({"registered": [a.model_dump(), b.model_dump()], "bridges": [x.model_dump() for x in bridges]})

if __name__ == "__main__":
    main()
