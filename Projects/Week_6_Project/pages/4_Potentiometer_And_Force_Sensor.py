import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import numpy as np
import streamlit as st
from core.potentiometer import output_voltage
from core.force_sensor import cantilever_deflection, cantilever_load, apply_calibration_matrix

st.set_page_config(page_title="Potentiometer & Force Sensor", page_icon="⚡", layout="wide")
st.title("⚡ Potentiometer & Force/Moment Sensor")

tab1, tab2, tab3 = st.tabs(["Potentiometer", "Cantilever Deflection", "Calibration Matrix"])

with tab1:
    st.markdown("A voltage divider: Vin/R = Vout/r.")
    col1, col2, col3 = st.columns(3)
    v_in = col1.number_input("Vin", min_value=0.0, value=5.0)
    r_total = col2.number_input("Total resistance R", min_value=0.01, value=1000.0)
    r_partial = col3.number_input("Partial resistance r (wiper position)", min_value=0.0, value=400.0)
    v_out = output_voltage(v_in, r_partial, r_total)
    st.metric("Vout", f"{v_out:.4f} V")

with tab2:
    st.markdown(
        "Cantilever beam formula (within the elastic limit): "
        "delta = (P * L^3) / (3 * E * I)."
    )
    col4, col5, col6, col7 = st.columns(4)
    p = col4.number_input("Load P", min_value=0.0, value=10.0)
    length = col5.number_input("Bar length L", min_value=0.01, value=0.05)
    e_mod = col6.number_input("Young's modulus E", min_value=0.01, value=200e9, format="%.3e")
    i_mom = col7.number_input("Second moment of area I", min_value=1e-15, value=1e-9, format="%.3e")

    delta = cantilever_deflection(p, length, e_mod, i_mom)
    st.metric("Deflection (delta)", f"{delta:.3e}")

    recovered_p = cantilever_load(delta, length, e_mod, i_mom)
    st.caption(f"Round-trip check: solving for P from that deflection gives {recovered_p:.4f} (should match the input load).")

with tab3:
    st.markdown(
        "Eight raw strain-gauge readings (W1..W8) are combined into the "
        "six force/moment components via a 6x8 calibration matrix: "
        "[F] = C_M * [W]."
    )
    st.caption("Enter 8 raw readings and a 6x8 calibration matrix (defaults to a simple scaled-identity-like example).")

    raw = []
    cols = st.columns(8)
    for i in range(8):
        raw.append(cols[i].number_input(f"W{i+1}", value=1.0, key=f"w_{i}"))

    default_cm = np.zeros((6, 8))
    for i in range(6):
        default_cm[i, i % 8] = 1.0
        default_cm[i, (i + 4) % 8] = -1.0

    cm = np.zeros((6, 8))
    labels = ["Fx", "Fy", "Fz", "Mx", "My", "Mz"]
    for i in range(6):
        row_cols = st.columns(8)
        for j in range(8):
            cm[i, j] = row_cols[j].number_input(f"{labels[i]} x W{j+1}", value=float(default_cm[i, j]), key=f"cm_{i}_{j}")

    result = apply_calibration_matrix(raw, cm)
    st.subheader("Computed forces and moments")
    cols2 = st.columns(6)
    for i, label in enumerate(labels):
        cols2[i].metric(label, f"{result[i]:.3f}")
