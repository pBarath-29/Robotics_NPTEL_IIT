import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from core.edge_detection import threshold, apply_mask, gradient_magnitude, GX_MASK, GY_MASK, LAPLACIAN_MASK

st.set_page_config(page_title="Thresholding & Edge Detection", page_icon="🔲", layout="wide")
st.title("🔲 Thresholding & Edge Detection")

tab1, tab2 = st.tabs(["Thresholding", "Edge Detection"])

size = 12
rng = np.random.default_rng(3)
background = rng.uniform(0, 60, size=(size, size))
image = background.copy()
image[3:9, 3:9] = rng.uniform(180, 255, size=(6, 6))  # a bright square "object"

with tab1:
    st.markdown(
        "For a white object on a dark background: P(x,y) > T becomes 1 "
        "(object), otherwise 0 (background)."
    )
    t = st.slider("Threshold T", 0, 255, 120)
    binary = threshold(image, t)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Raw intensity")
        fig1, ax1 = plt.subplots()
        im1 = ax1.imshow(image, cmap="gray", vmin=0, vmax=255)
        fig1.colorbar(im1, ax=ax1)
        st.pyplot(fig1)
    with col2:
        st.subheader("Binary silhouette")
        fig2, ax2 = plt.subplots()
        ax2.imshow(binary, cmap="gray", vmin=0, vmax=1)
        st.pyplot(fig2)

with tab2:
    st.markdown(
        "Gx and Gy approximate the horizontal/vertical derivatives; the "
        "Laplacian uses second-order derivatives for sharper edges."
    )
    mask_choice = st.selectbox("Mask", ["Gx", "Gy", "Laplacian", "Gradient magnitude (Gx + Gy)"])

    if mask_choice == "Gx":
        result = apply_mask(image, GX_MASK)
    elif mask_choice == "Gy":
        result = apply_mask(image, GY_MASK)
    elif mask_choice == "Laplacian":
        result = apply_mask(image, LAPLACIAN_MASK)
    else:
        result = gradient_magnitude(image)

    col3, col4 = st.columns(2)
    with col3:
        st.subheader("Original")
        fig3, ax3 = plt.subplots()
        im3 = ax3.imshow(image, cmap="gray", vmin=0, vmax=255)
        fig3.colorbar(im3, ax=ax3)
        st.pyplot(fig3)
    with col4:
        st.subheader(f"{mask_choice} response")
        fig4, ax4 = plt.subplots()
        im4 = ax4.imshow(result, cmap="gray")
        fig4.colorbar(im4, ax=ax4)
        st.pyplot(fig4)
