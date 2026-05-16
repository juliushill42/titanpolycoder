import json, hashlib
from pathlib import Path

class Node:
    def __init__(self, pattern_id, runtime="python", root=Path(__file__).resolve().parents[2]):
        self.pattern_id = pattern_id
        self.runtime = runtime
        self.root = root
        self.state = root / "data" / f"{pattern_id}.json"
        self.state.parent.mkdir(parents=True, exist_ok=True)

    def code_hash(self):
        return hashlib.sha256((self.pattern_id + self.runtime).encode()).hexdigest()

    def heartbeat(self):
        payload = {"pattern_id": self.pattern_id, "runtime": self.runtime, "code_hash": self.code_hash()}
        self.state.write_text(json.dumps(payload, indent=2))
        return payload

    def run_task(self, task: dict):
        return {"pattern_id": self.pattern_id, "task": task, "result": f"processed:{task.get('name', 'task')}"}
