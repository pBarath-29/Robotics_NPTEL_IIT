import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import numpy as np
import streamlit as st
from core.transformations import rot_x, rot_y, rot_z, trans, compose, apply_to_point, invert

st.set_page_config(page_title="Frame Transformation", page_icon="🧭", layout="wide")
st.title("🧭 Frame Transformation")

st.markdown(
    """
Build a sequence of elementary translation and rotation operators, the same
way a combined transformation is built up from Trans(a, b, c) and
Rot(axis, theta) operators in the notes. The operators are applied in the
order listed, and combined into a single 4x4 homogeneous transformation
matrix.
"""
)

num_steps = st.number_input("Number of operators in the sequence", min_value=1, max_value=6, value=2, step=1)

matrices = []
st.subheader("Sequence")
for i in range(int(num_steps)):
    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
    with col1:
        op_type = st.selectbox(f"Step {i+1} operator", ["Translate", "Rotate X", "Rotate Y", "Rotate Z"], key=f"op_{i}")
    if op_type == "Translate":
        with col2:
            a = st.number_input("a", value=0.0, key=f"a_{i}")
        with col3:
            b = st.number_input("b", value=0.0, key=f"b_{i}")
        with col4:
            c = st.number_input("c", value=0.0, key=f"c_{i}")
        matrices.append(trans(a, b, c))
    else:
        with col2:
            theta_deg = st.number_input("theta (degrees)", value=0.0, key=f"theta_{i}")
        theta_rad = np.deg2rad(theta_deg)
        if op_type == "Rotate X":
            matrices.append(rot_x(theta_rad))
        elif op_type == "Rotate Y":
            matrices.append(rot_y(theta_rad))
        else:
            matrices.append(rot_z(theta_rad))

st.divider()

col_a, col_b, col_c = st.columns(3)
px = col_a.number_input("Point x (body frame)", value=1.0)
py = col_b.number_input("Point y (body frame)", value=0.0)
pz = col_c.number_input("Point z (body frame)", value=0.0)

combined = compose(matrices)
q_u = apply_to_point(combined, (px, py, pz))

st.subheader("Composed 4x4 transformation matrix")
st.dataframe(combined)

st.subheader("Transformed point")
st.markdown(f"Q_U = ({q_u[0]:.4f}, {q_u[1]:.4f}, {q_u[2]:.4f})")

with st.expander("Show the inverse transformation"):
    inv = invert(combined)
    st.dataframe(inv)
    check = combined @ inv
    st.caption("Transform times its inverse should equal the identity matrix:")
    st.dataframe(np.round(check, 10))
