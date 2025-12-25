import math
import numpy as np
from .config import GRID_N, ALT_BANDS
from .utils import rng_for_tick, clamp

def smooth_noise(rng, shape, passes=2):
    x = rng.normal(0.0, 1.0, size=shape)
    for _ in range(passes):
        x = (
            x
            + np.roll(x, 1, -1) + np.roll(x, -1, -1)
            + np.roll(x, 1, -2) + np.roll(x, -1, -2)
        ) / 5.0
    x = (x - x.min()) / (x.max() - x.min() + 1e-9)
    return x

def evolve_field(state, dispersion: float, breathing: float):
    rng = rng_for_tick(state.rng_seed, state.tick + 1)

    if state.field_prob is None:
        base = smooth_noise(rng, (ALT_BANDS, GRID_N, GRID_N))
        state.field_prob = 0.08 + 0.35 * base
        state.field_conf = 0.7 + 0.25 * (1 - base)

    prob = state.field_prob.copy()
    conf = state.field_conf.copy()

    prob += smooth_noise(rng, prob.shape, 1) * 0.05
    prob = np.clip(prob, 0, 1)

    conf -= 0.1 * dispersion
    conf -= 0.05 * breathing
    conf = np.clip(conf, 0.05, 0.98)

    state.field_prob = prob
    state.field_conf = conf
    return prob, conf
