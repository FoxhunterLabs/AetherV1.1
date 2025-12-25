from dataclasses import replace
from aether.core.models import EngineState
from aether.core.engine import step_engine

def replay(
    seed: int,
    ticks: int,
    dispersion: float,
    breathing: float,
    run_id: int = 0,
):
    state = EngineState(run_id=run_id, rng_seed=seed)

    for _ in range(ticks):
        state = step_engine(state, dispersion=dispersion, breathing=breathing)

    return state
