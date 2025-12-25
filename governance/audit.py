import json, hashlib
from dataclasses import dataclass
from typing import Dict, Any, List
from datetime import datetime

@dataclass(frozen=True)
class AuditEntry:
    tick: int
    timestamp: str
    event_type: str
    payload: Dict[str, Any]
    prev_hash: str
    hash: str

class AuditChain:
    def __init__(self, limit=140):
        self.entries: List[AuditEntry] = []
        self.limit = limit

    def append(self, tick: int, event_type: str, payload: Dict[str, Any]):
        prev = self.entries[-1].hash if self.entries else "0"*64
        data = {
            "tick": tick,
            "timestamp": datetime.utcnow().isoformat()+"Z",
            "event_type": event_type,
            "payload": payload,
            "prev_hash": prev,
        }
        h = hashlib.sha256(
            json.dumps(data, sort_keys=True, default=str).encode()
        ).hexdigest()

        self.entries.append(
            AuditEntry(
                tick=data["tick"],
                timestamp=data["timestamp"],
                event_type=event_type,
                payload=payload,
                prev_hash=prev,
                hash=h,
            )
        )
        self.entries[:] = self.entries[-self.limit:]
