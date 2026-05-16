from pydantic import BaseModel, Field
from typing import Any, Optional

class PatternSpec(BaseModel):
    pattern_id: str
    parent_id: Optional[str] = None
    domain: str
    function: str
    runtime: str
    code_hash: str
    key_fingerprint: str = ""
    rules: dict[str, Any] = Field(default_factory=dict)
    fitness: float = 0.0
