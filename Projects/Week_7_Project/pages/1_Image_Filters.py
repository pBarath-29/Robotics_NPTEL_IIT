import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from core.image_filters import average_filter, median_filter

st.set_page_config(page_title="Image Filters", page_icon="🧹", layout="wide")
st.title("🧹 Image Filters")

st.markdown(
    """
Neighborhood averaging replaces each pixel with the mean of its
neighborhood, using only the pixels that actually exist within the image
(so edge and corner pixels average over fewer pixels). Median filtering
replaces each pixel with the median of its neighborhood instead, which
removes "salt and pepper" noise spikes without blurring edges.
"""
)

size = st.slider("Grid size (n x n)", 3, 8, 5)
filter_type = st.radio("Filter", ["Averaging", "Median"])

st.subheader("Image pixel intensities")
default_image = np.random.default_rng(7).integers(0, 256, size=(size, size)).astype(float)
if st.button("Add a salt-and-pepper spike to the center pixel"):
    default_image[size // 2, size // 2] = 255.0

image = np.zeros((size, size))
for i in range(size):
    cols = st.columns(size)
    for j in range(size):
        image[i, j] = cols[j].number_input(
            f"({i},{j})", min_value=0.0, max_value=255.0,
            value=float(default_image[i, j]), key=f"px_{i}_{j}", label_visibility="collapsed",
        )

result = average_filter(image) if filter_type == "Averaging" else median_filter(image)

col1, col2 = st.columns(2)
with col1:
    st.subheader("Original")
    fig1, ax1 = plt.subplots()
    im1 = ax1.imshow(image, cmap="gray", vmin=0, vmax=255)
    fig1.colorbar(im1, ax=ax1)
    st.pyplot(fig1)
with col2:
    st.subheader(f"After {filter_type.lower()} filter")
    fig2, ax2 = plt.subplots()
    im2 = ax2.imshow(result, cmap="gray", vmin=0, vmax=255)
    fig2.colorbar(im2, ax=ax2)
    st.pyplot(fig2)
