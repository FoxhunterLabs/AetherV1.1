import streamlit as st
import pandas as pd

def render_timeline(state):
    st.subheader("Timeline")
    df = pd.DataFrame([s.__dict__ for s in state.history]).tail(200)
    st.line_chart(df[["clarity", "risk", "predicted_risk"]])
