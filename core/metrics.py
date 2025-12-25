import numpy as np
from .utils import clamp

def compute_metrics(state, prob, conf):
    mean_prob = float(prob.mean())
    mean_conf = float(conf.mean())
    max_prob = float(prob.max())
    min_conf = float(conf.min())

    raw_clarity = clamp(mean_conf - 0.3 * max_prob, 0, 1)
    state.clarity_ema = 0.15 * raw_clarity + 0.85 * state.clarity_ema
    clarity = state.clarity_ema * 100

    uncertainty = float((1 - conf).mean())
    risk = clamp(
        mean_prob * 60 + uncertainty * 70 + (100 - clarity) * 0.25,
        0, 100
    )

    predicted = clamp(risk * 0.75 + max_prob * 25, 0, 100)

    if clarity > 85 and risk < 40:
        state_class = "STABLE"
    elif clarity > 70:
        state_class = "TENSE"
    elif clarity > 55:
        state_class = "HIGH_RISK"
    else:
        state_class = "CRITICAL"

    return round(clarity,1), round(risk,1), round(predicted,1), state_class
