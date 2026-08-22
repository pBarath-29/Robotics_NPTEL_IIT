import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from core.vision import apply_mask, SHARPEN_MASK

st.set_page_config(page_title="Image Masking", page_icon="🖼️", layout="wide")
st.title("🖼️ Image Masking (Convolution)")

st.markdown(
    """
A 3x3 mask of coefficients is centered on each pixel. Each coefficient is
multiplied by the raw intensity beneath it, and the 9 products are summed
to give the new pre-processed pixel value. Mask coefficients that fall
outside the image boundary contribute 0.
"""
)

size = st.slider("Grid size (n x n)", 3, 8, 5)

st.subheader("Image pixel intensities")
image = np.zeros((size, size))
default_image = np.random.default_rng(42).integers(0, 256, size=(size, size)).astype(float)
for i in range(size):
    cols = st.columns(size)
    for j in range(size):
        image[i, j] = cols[j].number_input(
            f"({i},{j})", min_value=0.0, max_value=255.0,
            value=float(default_image[i, j]), key=f"px_{i}_{j}", label_visibility="collapsed",
        )

st.subheader("3x3 mask")
default_mask = SHARPEN_MASK
mask = np.zeros((3, 3))
for i in range(3):
    cols = st.columns(3)
    for j in range(3):
        mask[i, j] = cols[j].number_input(
            f"mask_{i}_{j}", value=float(default_mask[i, j]), key=f"mask_{i}_{j}", label_visibility="collapsed",
        )
st.caption(f"Sum of mask coefficients: {mask.sum():.2f} (many noise-reduction masks sum to 0).")

result = apply_mask(image, mask)

col1, col2 = st.columns(2)
with col1:
    st.subheader("Original")
    fig1, ax1 = plt.subplots()
    im1 = ax1.imshow(image, cmap="gray", vmin=0, vmax=255)
    fig1.colorbar(im1, ax=ax1)
    st.pyplot(fig1)
with col2:
    st.subheader("Pre-processed")
    fig2, ax2 = plt.subplots()
    im2 = ax2.imshow(result, cmap="gray")
    fig2.colorbar(im2, ax=ax2)
    st.pyplot(fig2)
