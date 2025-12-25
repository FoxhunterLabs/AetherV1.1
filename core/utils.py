import json, hashlib
from datetime import datetime
from typing import Dict, Any
import numpy as np

def clamp(v: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, v))

def utc_now() -> str:
    return datetime.utcnow().isoformat() + "Z"

def sha256_hash(data: Dict[str, Any]) -> str:
    s = json.dumps(data, sort_keys=True, default=str)
    return hashlib.sha256(s.encode()).hexdigest()

def rng_for_tick(seed: int, tick: int) -> np.random.Generator:
    return np.random.default_rng((seed + tick) % (2**32))
