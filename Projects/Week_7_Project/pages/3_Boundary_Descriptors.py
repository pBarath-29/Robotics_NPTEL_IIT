import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from core.boundary_descriptors import (
    DIRECTIONS_4,
    DIRECTIONS_8,
    encode_chain,
    circle_signature,
    square_signature,
    compactness,
    REFERENCE_COMPACTNESS,
    closest_shape_match,
)

st.set_page_config(page_title="Boundary Descriptors", page_icon="🔗", layout="wide")
st.title("🔗 Boundary Descriptors")

tab1, tab2, tab3 = st.tabs(["Chain Code", "Signature", "Compactness"])

with tab1:
    st.markdown(
        "Traces a closed boundary as a sequence of fixed-length unit "
        "steps. Enter integer grid points for a simple closed shape "
        "(the last point connects back to the first)."
    )
    n_dir = st.radio("Directions", ["4-directional", "8-directional"])
    directions = DIRECTIONS_4 if n_dir == "4-directional" else DIRECTIONS_8

    default_shape = "0,0\n3,0\n3,1\n0,1" if n_dir == "4-directional" else "0,0\n2,0\n0,2"
    text = st.text_area("Boundary points (one 'x,y' pair per line)", value=default_shape)
    try:
        points = [tuple(int(v) for v in line.split(",")) for line in text.strip().splitlines()]
        codes = encode_chain(points, directions)
        st.markdown(f"**Chain code:** `{codes}`")

        xs = [p[0] for p in points] + [points[0][0]]
        ys = [p[1] for p in points] + [points[0][1]]
        fig, ax = plt.subplots()
        ax.plot(xs, ys, marker="o")
        ax.set_aspect("equal")
        ax.grid(True, linestyle="--", alpha=0.4)
        st.pyplot(fig)
    except (ValueError, IndexError) as e:
        st.error(f"Could not parse boundary points: {e}")

with tab2:
    st.markdown("A signature plots distance r from the center to the boundary as a function of angle theta.")
    shape = st.radio("Shape", ["Circle", "Square"])
    a = st.number_input("A (circle radius / square half-side)", min_value=0.1, value=3.0)
    theta = np.linspace(0, 2 * np.pi, 300)
    r = circle_signature(theta, a) if shape == "Circle" else square_signature(theta, a)

    fig2, ax2 = plt.subplots()
    ax2.plot(np.rad2deg(theta), r)
    ax2.set_xlabel("theta (deg)")
    ax2.set_ylabel("r")
    ax2.grid(True, linestyle="--", alpha=0.4)
    st.pyplot(fig2)

with tab3:
    st.markdown("Compactness = Perimeter^2 / Area, compared against known reference shapes.")
    col1, col2 = st.columns(2)
    perimeter = col1.number_input("Perimeter", min_value=0.01, value=20.0)
    area = col2.number_input("Area", min_value=0.01, value=25.0)
    c = compactness(perimeter, area)
    st.metric("Compactness", f"{c:.4f}")

    st.subheader("Reference values")
    for name, value in REFERENCE_COMPACTNESS.items():
        st.markdown(f"**{name}**: {value:.4f}")

    match = closest_shape_match(c)
    st.success(f"Closest match: **{match}**")
