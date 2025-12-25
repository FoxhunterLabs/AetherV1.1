from dataclasses import dataclass, field
from typing import Dict, Any, Literal, List
from datetime import datetime

Level = Literal["INFO", "WARN", "ALERT"]

@dataclass(frozen=True)
class EventRecord:
    timestamp: str
    level: Level
    msg: str
    extras: Dict[str, Any] = field(default_factory=dict)

class EventLog:
    def __init__(self, limit=240):
        self.events: List[EventRecord] = []
        self.limit = limit

    def log(self, level: Level, msg: str, extras=None):
        self.events.append(
            EventRecord(
                timestamp=datetime.utcnow().strftime("%H:%M:%S"),
                level=level,
                msg=msg,
                extras=extras or {}
            )
        )
        self.events[:] = self.events[-self.limit:]
