import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import numpy as np
import streamlit as st
from core.dh import (
    forward_kinematics,
    two_dof_planar_dh_table,
    two_dof_planar_expected_position,
    minimover_dh_table,
)

st.set_page_config(page_title="DH Forward Kinematics", page_icon="⚙️", layout="wide")
st.title("⚙️ DH Forward Kinematics")

st.markdown(
    """
Build a Denavit-Hartenberg table, one row per joint, and compute the final
position and orientation of the end-effector. Each row's transform is built
from two screw motions: rotate about Z by theta then translate along Z by
d, followed by rotate about X by alpha then translate along X by a.
"""
)

example = st.selectbox(
    "Load an example",
    ["Custom", "2-DoF planar arm (Lecture 4)", "MINIMOVER 5-DoF (Lecture 5)"],
)

if example == "2-DoF planar arm (Lecture 4)":
    col1, col2 = st.columns(2)
    l1 = col1.number_input("L1", min_value=0.0, value=3.0)
    l2 = col2.number_input("L2", min_value=0.0, value=2.0)
    col3, col4 = st.columns(2)
    theta1_deg = col3.number_input("theta1 (degrees)", value=30.0)
    theta2_deg = col4.number_input("theta2 (degrees)", value=45.0)
    theta1, theta2 = np.deg2rad(theta1_deg), np.deg2rad(theta2_deg)
    dh_table = two_dof_planar_dh_table(l1, l2, theta1, theta2)
    expected = two_dof_planar_expected_position(l1, l2, theta1, theta2)
elif example == "MINIMOVER 5-DoF (Lecture 5)":
    col1, col2 = st.columns(2)
    l1 = col1.number_input("L1", min_value=0.0, value=2.0)
    l2 = col2.number_input("L2", min_value=0.0, value=1.5)
    thetas_deg = []
    cols = st.columns(5)
    for i in range(5):
        thetas_deg.append(cols[i].number_input(f"theta{i+1} (deg)", value=10.0 * (i + 1), key=f"mm_{i}"))
    thetas = [np.deg2rad(t) for t in thetas_deg]
    dh_table = minimover_dh_table(l1, l2, thetas)
    expected = None
else:
    num_joints = st.number_input("Number of joints", min_value=1, max_value=6, value=2, step=1)
    dh_table = []
    for i in range(int(num_joints)):
        st.markdown(f"**Joint {i+1}**")
        cols = st.columns(4)
        theta_deg = cols[0].number_input("theta (deg)", value=0.0, key=f"theta_{i}")
        d = cols[1].number_input("d", value=0.0, key=f"d_{i}")
        alpha_deg = cols[2].number_input("alpha (deg)", value=0.0, key=f"alpha_{i}")
        a = cols[3].number_input("a", value=1.0, key=f"a_{i}")
        dh_table.append({
            "theta": np.deg2rad(theta_deg), "d": d,
            "alpha": np.deg2rad(alpha_deg), "a": a,
        })
    expected = None

t_final, frames = forward_kinematics(dh_table)
position = t_final[:3, 3]

st.divider()
st.subheader("Final transformation matrix")
st.dataframe(t_final)

st.subheader("End-effector position")
c1, c2, c3 = st.columns(3)
c1.metric("x", f"{position[0]:.4f}")
c2.metric("y", f"{position[1]:.4f}")
c3.metric("z", f"{position[2]:.4f}")

if expected is not None:
    st.caption(
        f"Closed-form check from the notes: expected ({expected[0]:.4f}, "
        f"{expected[1]:.4f}, {expected[2]:.4f})."
    )
