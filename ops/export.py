import json
import pandas as pd
from typing import Dict, Any
from aether.core.models import EngineState
from aether.ops.snapshot import build_run_snapshot

def export_snapshot_json(state: EngineState, **kwargs) -> bytes:
    payload = build_run_snapshot(state, **kwargs)
    return json.dumps(payload, indent=2).encode("utf-8")

def export_metrics_csv(state: EngineState, tail: int = 400) -> bytes:
    if not state.history:
        return b""
    df = pd.DataFrame([s.__dict__ for s in state.history]).tail(tail)
    return df.to_csv(index=False).encode("utf-8")
