from typing import Any, Dict
from aether.core.models import EngineState
from aether.core.utils import utc_now
from aether.ops.serialize import make_json_safe

def build_run_snapshot(
    state: EngineState,
    ao: Dict[str, Any] | None = None,
    env_name: str = "Synthetic",
    gov_name: str = "Synthetic",
    note: str = "Synthetic, non-operational uncertainty visualization run.",
    history_tail: int = 400,
    events_tail: int = 120,
    audit_tail: int = 120,
) -> Dict[str, Any]:
    hist = [s.__dict__ for s in state.history][-history_tail:]

    payload = {
        "generated_at_utc": utc_now(),
        "run_id": state.run_id,
        "rng_seed": state.rng_seed,
        "ao": ao or {"label": "Synthetic AO"},
        "environment": env_name,
        "governance": gov_name,
        "note": note,
        "history_tail": hist,
        "events_tail": [e.__dict__ for e in state.events.events][-events_tail:],
        "audit_tail": [a.__dict__ for a in state.audit.entries][-audit_tail:],
    }
    return make_json_safe(payload)
