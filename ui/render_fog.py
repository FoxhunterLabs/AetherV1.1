import streamlit as st
import plotly.graph_objects as go
import numpy as np

def render_fog(prob, conf):
    st.subheader("Volumetric Fog (Experimental)")
    z = prob.flatten()
    fig = go.Figure(go.Scatter3d(
        x=np.random.rand(len(z)),
        y=np.random.rand(len(z)),
        z=z * 10000,
        mode="markers",
        marker=dict(size=2, opacity=0.15)
    ))
    st.plotly_chart(fig, use_container_width=True)
