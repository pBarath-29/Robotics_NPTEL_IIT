import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import numpy as np
import streamlit as st
from core.inverse_kinematics import solve_2dof, UnreachableTarget
from core.dh import two_dof_planar_dh_table, forward_kinematics

st.set_page_config(page_title="Inverse Kinematics", page_icon="🎯", layout="wide")
st.title("🎯 Inverse Kinematics")

st.markdown(
    """
For a 2-DoF planar arm, find the joint angles needed to reach a target
point. There are usually two solutions: a right-hand (elbow up) and a
left-hand (elbow down) configuration.
"""
)

col1, col2 = st.columns(2)
l1 = col1.number_input("L1", min_value=0.01, value=3.0)
l2 = col2.number_input("L2", min_value=0.01, value=2.0)

col3, col4 = st.columns(2)
qx = col3.number_input("Target x", value=4.0)
qy = col4.number_input("Target y", value=2.0)

try:
    solutions = solve_2dof(l1, l2, qx, qy)
except UnreachableTarget as e:
    st.error(str(e))
else:
    for theta1, theta2, label in solutions:
        st.subheader(label)
        c1, c2 = st.columns(2)
        c1.metric("theta1", f"{np.rad2deg(theta1):.2f} deg")
        c2.metric("theta2", f"{np.rad2deg(theta2):.2f} deg")

        dh_table = two_dof_planar_dh_table(l1, l2, theta1, theta2)
        t_final, _ = forward_kinematics(dh_table)
        reached = t_final[:3, 3]
        st.caption(
            f"Forward kinematics check: these angles reach "
            f"({reached[0]:.4f}, {reached[1]:.4f}), target was ({qx}, {qy})."
        )
