import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import streamlit as st
from core.performance import (
    BRU_UNIT_PRESETS,
    control_resolution_deg,
    programming_resolution,
    accuracy_repeatability_demo,
)

st.set_page_config(page_title="Performance Specs", page_icon="📏", layout="wide")
st.title("📏 Performance Specifications")

tab1, tab2, tab3 = st.tabs(["Resolution (BRU)", "Control Resolution (Encoder)", "Accuracy vs. Repeatability"])

with tab1:
    st.subheader("Programming resolution")
    st.markdown(
        "The smallest allowable position increment in computer programming, "
        "expressed in **Basic Resolution Units (BRU)**. The notes give three "
        "example BRU sizes: 0.01 inch, 0.001 mm, or 0.1 degree."
    )
    preset = st.selectbox("BRU size", list(BRU_UNIT_PRESETS.keys()))
    num_brus = st.number_input("Number of BRUs commanded", min_value=1, value=100, step=1)
    result = programming_resolution(BRU_UNIT_PRESETS[preset], num_brus)
    st.metric("Smallest programmable increment", f"{result:g} {preset.split()[-1]}")

with tab2:
    st.subheader("Control resolution from an optical encoder")
    st.markdown(
        "Control resolution is determined by the hardware feedback device. "
        "Notes example: an encoder reading 1000 pulses per 360-degree "
        "rotation yields 0.36 deg/pulse."
    )
    ppr = st.number_input("Pulses per revolution", min_value=1, value=1000, step=1)
    res = control_resolution_deg(ppr)
    st.metric("Control resolution", f"{res:.4f} deg/pulse")

with tab3:
    st.subheader("Accuracy vs. Repeatability")
    st.markdown(
        """
        - **Accuracy**: the deviation between the theoretical calculated
          point and the actual point reached.
        - **Repeatability**: the deviation across multiple attempts to
          return to the same taught point.

        Adjust the sliders to see how each concept looks differently on a
        scatter of simulated attempts at reaching one target point.
        """
    )
    c1, c2, c3 = st.columns(3)
    offset_x = c1.slider("Systematic offset X (accuracy error)", -2.0, 2.0, 0.6, 0.1)
    offset_y = c1.slider("Systematic offset Y (accuracy error)", -2.0, 2.0, 0.3, 0.1)
    repeatability_std = c2.slider("Repeatability spread (std dev)", 0.0, 1.0, 0.15, 0.05)
    n_attempts = c3.slider("Number of repeated attempts", 5, 100, 20, 5)

    fig, accuracy_dist = accuracy_repeatability_demo(
        target=(0.0, 0.0),
        accuracy_offset=(offset_x, offset_y),
        repeatability_std=repeatability_std,
        n_attempts=n_attempts,
    )
    st.pyplot(fig)
    st.caption(
        f"Accuracy (target to mean-landing-point distance): {accuracy_dist:.3f}. "
        f"Repeatability (scatter std dev around the mean landing point): {repeatability_std:.3f}."
    )
