from .models import AirspaceSnapshot
from .utils import utc_now
from .config import DT_SECONDS
from .field import evolve_field
from .metrics import compute_metrics

def step_engine(state, dispersion: float, breathing: float):
    state.sim_time_s += DT_SECONDS

    prob, conf = evolve_field(state, dispersion, breathing)
    clarity, risk, pred, status = compute_metrics(state, prob, conf)

    snap = AirspaceSnapshot(
        tick=state.tick + 1,
        utc_timestamp=utc_now(),
        sim_time_s=state.sim_time_s,
        ao_label="Synthetic AO",
        env="Synthetic",
        gov="Synthetic",
        clarity=clarity,
        risk=risk,
        predicted_risk=pred,
        state=status,
        mean_prob=float(prob.mean()),
        mean_conf=float(conf.mean()),
        max_prob=float(prob.max()),
        min_conf=float(conf.min()),
        dispersion=dispersion,
    )

    state.tick += 1
    state.history.append(snap)
    return state
