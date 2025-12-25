import streamlit as st
import pydeck as pdk
import pandas as pd
import numpy as np

def render_columns(prob, conf):
    st.subheader("3D Column Field")
    h = prob.mean(axis=0)

    df = pd.DataFrame({
        "lat": np.linspace(35, 36, h.shape[0]),
        "lon": np.linspace(-104, -103, h.shape[1]),
        "height": h.flatten() * 4000
    })

    layer = pdk.Layer(
        "ColumnLayer",
        data=df,
        get_position=["lon", "lat"],
        get_elevation="height",
        radius=150,
        elevation_scale=1,
        get_fill_color=[180, 80, 80, 140]
    )

    st.pydeck_chart(pdk.Deck(layers=[layer]))
