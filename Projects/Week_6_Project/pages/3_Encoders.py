import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import streamlit as st
from core.encoders import (
    absolute_encoder_divisions,
    absolute_encoder_resolution_deg,
    absolute_encoder_binary_code,
    incremental_encoder_direction,
)

st.set_page_config(page_title="Encoders", page_icon="🔢", layout="wide")
st.title("🔢 Encoders")

tab1, tab2 = st.tabs(["Absolute Encoder", "Incremental Encoder"])

with tab1:
    st.markdown(
        "Each of n concentric rings is one bit, giving 2^n divisions of "
        "the full rotation. The outermost ring is the least significant bit."
    )
    n_rings = st.slider("Number of rings (n)", 1, 16, 10)
    divisions = absolute_encoder_divisions(n_rings)
    resolution = absolute_encoder_resolution_deg(n_rings)

    col1, col2 = st.columns(2)
    col1.metric("Divisions (2^n)", divisions)
    col2.metric("Resolution", f"{resolution:.4f} deg/step")

    angle = st.slider("Angle to encode (deg)", 0.0, 360.0, 45.0)
    code = absolute_encoder_binary_code(angle, n_rings)
    st.markdown(f"**Binary code for {angle} deg:** `{code}`")

with tab2:
    st.markdown(
        "Uses one coded disc and two fixed photo-detectors (A, B). "
        "Whichever detector enters the dark zone first reveals the "
        "direction of rotation."
    )
    a_leads_b = st.radio("Which detector enters the dark zone first?", ["A", "B"]) == "A"
    direction = incremental_encoder_direction(a_leads_b)
    st.metric("Direction", direction)
