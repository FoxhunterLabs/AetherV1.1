from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional, Literal
import numpy as np

StateClass = Literal["STABLE", "TENSE", "HIGH_RISK", "CRITICAL"]

@dataclass(frozen=True)
class AirspaceSnapshot:
    tick: int
    utc_timestamp: str
    sim_time_s: float
    ao_label: str
    env: str
    gov: str
    clarity: float
    risk: float
    predicted_risk: float
    state: StateClass
    mean_prob: float
    mean_conf: float
    max_prob: float
    min_conf: float
    dispersion: float

@dataclass
class EngineState:
    tick: int = 0
    sim_time_s: float = 0.0
    run_id: int = 0
    rng_seed: int = 0

    field_prob: Optional[np.ndarray] = None
    field_conf: Optional[np.ndarray] = None

    history: List[AirspaceSnapshot] = field(default_factory=list)
    clarity_ema: float = 0.86
