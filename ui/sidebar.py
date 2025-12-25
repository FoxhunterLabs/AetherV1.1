import streamlit as st

def sidebar_controls():
    st.sidebar.markdown("### Controls")

    if st.sidebar.button("▶ Start"):
        st.session_state.running = True
    if st.sidebar.button("⏸ Pause"):
        st.session_state.running = False
    if st.sidebar.button("⟲ Reset"):
        st.session_state.clear()
        st.rerun()

    st.sidebar.markdown("---")
    dispersion = st.sidebar.slider("Dispersion", 0.0, 1.0, 0.35)
    breathing = st.sidebar.slider("Breathing", 0.0, 1.0, 0.55)
    volumetric = st.sidebar.checkbox("Volumetric Fog", value=True)

    return dispersion, breathing, volumetric
