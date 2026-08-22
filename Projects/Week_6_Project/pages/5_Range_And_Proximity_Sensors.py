import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import numpy as np
import streamlit as st
from core.range_sensor import triangulation_distance
from core.proximity_reference import PROXIMITY_SENSORS

st.set_page_config(page_title="Range & Proximity Sensors", page_icon="📏", layout="wide")
st.title("📏 Range & Proximity Sensors")

tab1, tab2 = st.tabs(["Triangulation Range Sensor", "Proximity Sensors"])

with tab1:
    st.markdown(
        "The emitter and receiver are separated by a fixed baseline 'a'. "
        "When the beam reflects perpendicular into the receiver, "
        "d = a * tan(theta)."
    )
    col1, col2 = st.columns(2)
    a = col1.number_input("Baseline a", min_value=0.01, value=0.1)
    theta_deg = col2.number_input("Beam angle theta (deg)", min_value=0.0, max_value=89.0, value=60.0)
    d = triangulation_distance(a, np.deg2rad(theta_deg))
    st.metric("Distance d", f"{d:.4f}")

with tab2:
    for name, info in PROXIMITY_SENSORS.items():
        with st.expander(name):
            st.markdown(f"**Target material:** {info['target_material']}")
            st.markdown(f"**Working principle:** {info['principle']}")
