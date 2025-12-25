import streamlit as st
import matplotlib.pyplot as plt

def render_cross_section(prob, conf):
    st.subheader("Cross Section")
    band = st.slider("Altitude Band", 0, prob.shape[0]-1, prob.shape[0]//2)
    fig, ax = plt.subplots()
    ax.imshow(prob[band], cmap="magma")
    ax.set_xticks([]); ax.set_yticks([])
    st.pyplot(fig)
