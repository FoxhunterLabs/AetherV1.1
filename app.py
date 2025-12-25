import time
import streamlit as st

from aether.core.engine import step_engine
from aether.core.models import EngineState

from aether.ui.layout import header, governance_banner
from aether.ui.sidebar import sidebar_controls
from aether.ui.timeline import render_timeline
from aether.ui.render_columns import render_columns
from aether.ui.render_fog import render_fog
from aether.ui.cross_section import render_cross_section

from aether.ops.export import (
    export_snapshot_json,
    export_metrics_csv,
)

# ------------------------------------------------------------
# Streamlit config
# ------------------------------------------------------------

st.set_page_config(
    page_title="AetherV1.1 — Synthetic Airspace Console",
    layout="wide",
)

# ------------------------------------------------------------
# Engine bootstrap
# ------------------------------------------------------------

def get_state() -> EngineState:
    if "engine" not in st.session_state:
        s = EngineState()
        s.run_id = int(time.time() * 1000)
        s.rng_seed = s.run_id % (2**32)
        st.session_state.engine = s
        st.session_state.running = False
    return st.session_state.engine


state = get_state()

# ------------------------------------------------------------
# Sidebar controls
# ------------------------------------------------------------

dispersion, breathing, volumetric = sidebar_controls()

# ------------------------------------------------------------
# Governance + header
# ------------------------------------------------------------

governance_banner()
header(state)

# ------------------------------------------------------------
# Simulation step
# ------------------------------------------------------------

if st.session_state.running:
    state = step_engine(
        state,
        dispersion=dispersion,
        breathing=breathing,
    )

# ------------------------------------------------------------
# Guard: no data yet
# ------------------------------------------------------------

if not state.history:
    st.info("Press **Start** to begin a synthetic run.")
    st.stop()

prob = state.field_prob
conf = state.field_conf
latest = state.history[-1]

# ------------------------------------------------------------
# Main views
# ------------------------------------------------------------

st.markdown("## Live Airspace Picture")

render_timeline(state)
render_cross_section(prob, conf)
render_columns(prob, conf)

if volumetric:
    render_fog(prob, conf)

# ------------------------------------------------------------
# Export block
# ------------------------------------------------------------

st.markdown("---")
st.subheader("Export (Synthetic Run Snapshot)")

snap_bytes = export_snapshot_json(state)
st.download_button(
    "Download Run Snapshot (JSON)",
    data=snap_bytes,
    file_name="aether_run_snapshot.json",
    mime="application/json",
    use_container_width=True,
)

csv_bytes = export_metrics_csv(state)
st.download_button(
    "Download Metrics (CSV)",
    data=csv_bytes,
    file_name="aether_metrics.csv",
    mime="text/csv",
    use_container_width=True,
)

# ------------------------------------------------------------
# Auto-rerun loop (streaming feel)
# ------------------------------------------------------------

if st.session_state.running:
    time.sleep(0.22)
    st.rerun()
