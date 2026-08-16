import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import numpy as np
import streamlit as st
from core.jacobian import jacobian, determinant, is_singular

st.set_page_config(page_title="Jacobian & Singularity", page_icon="🌀", layout="wide")
st.title("🌀 Jacobian & Singularity")

st.markdown(
    """
For a 2-DoF planar arm, the Jacobian relates joint velocities to
Cartesian velocities. A pose is singular when the determinant of the
Jacobian is zero, since the robot then loses a degree of freedom.
"""
)

col1, col2 = st.columns(2)
l1 = col1.number_input("L1", min_value=0.01, value=3.0)
l2 = col2.number_input("L2", min_value=0.01, value=2.0)

col3, col4 = st.columns(2)
theta1_deg = col3.number_input("theta1 (deg)", value=30.0)
theta2_deg = col4.number_input("theta2 (deg)", value=45.0)
theta1, theta2 = np.deg2rad(theta1_deg), np.deg2rad(theta2_deg)

j = jacobian(l1, l2, theta1, theta2)
det = determinant(l1, l2, theta1, theta2)
singular = is_singular(theta2)

st.subheader("Jacobian matrix")
st.dataframe(j)

col5, col6 = st.columns(2)
col5.metric("Determinant", f"{det:.4f}")
col6.metric("Singular?", "Yes" if singular else "No")

if singular:
    st.error(
        "This pose is singular. At theta2 = 0 deg the arm is fully "
        "stretched; at theta2 = 180 deg it is folded back. Either way, "
        "the robot behaves as a 1-DoF arm."
    )
else:
    st.success("This pose is not singular; the arm retains full 2-DoF mobility here.")

st.caption("Closed-form check from the notes: det(J) = L1 * L2 * sin(theta2).")
