from aether.core.models import AirspaceSnapshot, EngineState
from aether.core.utils import utc_now
from aether.core.config import DT_SECONDS
from aether.core.field import evolve_field
from aether.core.metrics import compute_metrics


def step_engine(
    state: EngineState,
    dispersion: float,
    breathing: float,
    ao_label: str = "Synthetic AO",
    env_name: str = "Synthetic",
    gov_name: str = "Synthetic",
) -> EngineState:
    """
    Advances the engine by one deterministic tick.
    No side effects outside EngineState.
    """

    # Advance clock
    state.sim_time_s += DT_SECONDS

    # Evolve synthetic field
    prob, conf = evolve_field(
        state,
        dispersion=dispersion,
        breathing=breathing,
    )

    # Compute governance metrics
    clarity, risk, predicted_risk, status = compute_metrics(
        state,
        prob,
        conf,
    )

    # Snapshot
    snap = AirspaceSnapshot(
        tick=state.tick + 1,
        utc_timestamp=utc_now(),
        sim_time_s=round(state.sim_time_s, 1),
        ao_label=ao_label,
        env=env_name,
        gov=gov_name,
        clarity=clarity,
        risk=risk,
        predicted_risk=predicted_risk,
        state=status,
        mean_prob=float(round(prob.mean(), 4)),
        mean_conf=float(round(conf.mean(), 4)),
        max_prob=float(round(prob.max(), 4)),
        min_conf=float(round(conf.min(), 4)),
        dispersion=float(round(dispersion, 3)),
    )

    # Persist
    state.tick = snap.tick
    state.history.append(snap)

    # Governance hooks
    if status in ("HIGH_RISK", "CRITICAL"):
        state.events.log(
            "ALERT",
            f"{status} @ tick {snap.tick}",
            {
                "clarity": clarity,
                "risk": risk,
                "predicted_risk": predicted_risk,
            },
        )
        state.audit.append(
            tick=snap.tick,
            event_type="risk_state",
            payload={
                "state": status,
                "clarity": clarity,
                "risk": risk,
                "predicted_risk": predicted_risk,
            },
        )

    return state
