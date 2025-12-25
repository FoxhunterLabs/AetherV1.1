from typing import Any, Dict
import numpy as np

def ndarray_to_list(x):
    if x is None:
        return None
    return x.astype(float).tolist()

def safe_float(v):
    try:
        return float(v)
    except Exception:
        return v

def make_json_safe(d: Dict[str, Any]) -> Dict[str, Any]:
    out = {}
    for k, v in d.items():
        if isinstance(v, np.ndarray):
            out[k] = ndarray_to_list(v)
        elif isinstance(v, dict):
            out[k] = make_json_safe(v)
        elif isinstance(v, list):
            out[k] = v
        else:
            out[k] = safe_float(v)
    return out
