import json
from typing import Any, Dict

def export_snapshot(payload: Dict[str, Any]) -> bytes:
    return json.dumps(payload, indent=2).encode("utf-8")
