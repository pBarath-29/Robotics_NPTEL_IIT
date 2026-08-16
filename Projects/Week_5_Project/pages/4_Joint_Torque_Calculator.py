import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import numpy as np
import streamlit as st
from core.inertia import circular_center_of_mass_izz
from core.dynamics import compute_torques, gravity_only_torques, potential_energy, DYNAMIC_COUPLING_SYMMETRY_HOLDS

st.set_page_config(page_title="Joint Torque Calculator", page_icon="🔩", layout="wide")
st.title("🔩 2-DoF Joint Torque Calculator")

st.markdown(
    """
Computes the joint torques needed to produce a given motion of a 2-link
planar arm, using the Center of Mass Lagrange-Euler method from Lecture 6.
Each link is treated as a uniform circular rod, so its moment of inertia
about its own center of mass comes straight from the Inertia Tensor page.
"""
)

st.subheader("Link properties")
col1, col2, col3, col4 = st.columns(4)
m1 = col1.number_input("m1 (mass of link 1)", min_value=0.01, value=2.0)
l1 = col2.number_input("L1 (length of link 1)", min_value=0.01, value=1.0)
r1 = col3.number_input("r1 (radius of link 1)", min_value=0.0, value=0.05)
g = col4.number_input("g (gravity)", value=9.81)

col5, col6, col7 = st.columns(3)
m2 = col5.number_input("m2 (mass of link 2)", min_value=0.01, value=1.5)
l2 = col6.number_input("L2 (length of link 2)", min_value=0.01, value=0.8)
r2 = col7.number_input("r2 (radius of link 2)", min_value=0.0, value=0.03)

i1 = circular_center_of_mass_izz(m1, r1, l1)
i2 = circular_center_of_mass_izz(m2, r2, l2)
st.caption(f"Computed I1 = {i1:.5f}, I2 = {i2:.5f} (circular link, center-of-mass frame).")

st.divider()
st.subheader("Motion state")
col8, col9 = st.columns(2)
theta1_deg = col8.number_input("theta1 (deg)", value=30.0)
theta2_deg = col9.number_input("theta2 (deg)", value=45.0)
col10, col11 = st.columns(2)
theta1_dot = col10.number_input("theta1' (rad/s)", value=0.5)
theta2_dot = col11.number_input("theta2' (rad/s)", value=-0.3)
col12, col13 = st.columns(2)
theta1_ddot = col12.number_input("theta1'' (rad/s^2)", value=0.1)
theta2_ddot = col13.number_input("theta2'' (rad/s^2)", value=0.2)

theta1, theta2 = np.deg2rad(theta1_deg), np.deg2rad(theta2_deg)
tau1, tau2 = compute_torques(theta1, theta2, theta1_dot, theta2_dot, theta1_ddot, theta2_ddot,
                              m1, m2, l1, l2, i1, i2, g)

st.divider()
st.subheader("Required joint torques")
col14, col15 = st.columns(2)
col14.metric("tau1", f"{tau1:.4f}")
col15.metric("tau2", f"{tau2:.4f}")

with st.expander("Consistency checks"):
    st.markdown(
        f"**Dynamic coupling symmetry (D12 = D21):** "
        f"{'holds' if DYNAMIC_COUPLING_SYMMETRY_HOLDS else 'does NOT hold'} "
        f"(checked symbolically once when this page loads)."
    )

    g_tau1, g_tau2 = gravity_only_torques(theta1, theta2, m1, m2, l1, l2, i1, i2, g)
    eps = 1e-6
    p0 = potential_energy(theta1, theta2, m1, m2, l1, l2, g)
    p1 = potential_energy(theta1 + eps, theta2, m1, m2, l1, l2, g)
    p2 = potential_energy(theta1, theta2 + eps, m1, m2, l1, l2, g)
    dp_dtheta1 = (p1 - p0) / eps
    dp_dtheta2 = (p2 - p0) / eps

    st.markdown(
        "At zero velocity and zero acceleration, torque must equal the "
        "gradient of the potential energy -- a property any correctly "
        "derived Lagrangian must satisfy."
    )
    c1, c2 = st.columns(2)
    c1.metric("tau1 (v=a=0)", f"{g_tau1:.4f}")
    c2.metric("Numeric dP/dtheta1", f"{dp_dtheta1:.4f}")
    c3, c4 = st.columns(2)
    c3.metric("tau2 (v=a=0)", f"{g_tau2:.4f}")
    c4.metric("Numeric dP/dtheta2", f"{dp_dtheta2:.4f}")
