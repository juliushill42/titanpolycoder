import json
from pathlib import Path
from .patterns import PatternSpec

class Registry:
    def __init__(self, root: Path):
        self.root = root
        self.path = root / "data" / "patterns.json"
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self.path.write_text("[]")

    def load(self) -> list[PatternSpec]:
        return [PatternSpec.model_validate(x) for x in json.loads(self.path.read_text())]

    def save(self, specs: list[PatternSpec]) -> None:
        self.path.write_text(json.dumps([s.model_dump() for s in specs], indent=2))

    def upsert(self, spec: PatternSpec) -> None:
        specs = self.load()
        specs = [s for s in specs if s.pattern_id != spec.pattern_id]
        specs.append(spec)
        self.save(specs)
