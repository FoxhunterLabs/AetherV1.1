import streamlit as st

WATERMARK = "SYNTHETIC — NOT OPERATIONAL"

def governance_banner():
    st.info(
        f"""
### {WATERMARK}
No live data · No control authority · No targeting  
UI-only uncertainty visualization
"""
    )

def header(state):
    st.markdown("## AetherV1.1")
    st.caption(f"Run ID: {state.run_id} · Seed: {state.rng_seed}")
