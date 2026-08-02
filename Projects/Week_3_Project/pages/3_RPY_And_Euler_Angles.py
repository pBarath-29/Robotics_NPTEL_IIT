import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import numpy as np
import streamlit as st
from core.orientation import rpy_to_matrix, matrix_to_rpy, euler_to_matrix, matrix_to_euler

st.set_page_config(page_title="RPY & Euler Angles", page_icon="📐", layout="wide")
st.title("📐 RPY & Euler Angles")

st.markdown(
    """
Roll-Pitch-Yaw angles rotate about the fixed universal axes. Euler angles
rotate about the body's own moving axes instead. Pick a convention, choose
whether to build a matrix from angles or extract angles from a matrix.
"""
)

convention = st.radio("Convention", ["Roll-Pitch-Yaw", "Euler"])
direction = st.radio("Direction", ["Angles -> Matrix", "Matrix -> Angles"])

if direction == "Angles -> Matrix":
    col1, col2, col3 = st.columns(3)
    a_deg = col1.number_input("alpha (degrees)", value=20.0)
    b_deg = col2.number_input("beta (degrees)", value=30.0)
    g_deg = col3.number_input("gamma (degrees)", value=40.0)
    a, b, g = np.deg2rad(a_deg), np.deg2rad(b_deg), np.deg2rad(g_deg)

    if convention == "Roll-Pitch-Yaw":
        matrix = rpy_to_matrix(a, b, g)
    else:
        matrix = euler_to_matrix(a, b, g)

    st.subheader("Resulting orientation matrix")
    st.dataframe(matrix)

else:
    st.caption("Enter each element of the 3x3 orientation matrix.")
    matrix = np.eye(3)
    for i in range(3):
        cols = st.columns(3)
        for j in range(3):
            matrix[i, j] = cols[j].number_input(f"r[{i+1}][{j+1}]", value=float(np.eye(3)[i, j]), key=f"em_{i}_{j}")

    if convention == "Roll-Pitch-Yaw":
        a, b, g = matrix_to_rpy(matrix)
    else:
        a, b, g = matrix_to_euler(matrix)

    st.subheader("Extracted angles")
    c1, c2, c3 = st.columns(3)
    c1.metric("alpha", f"{np.rad2deg(a):.2f} deg")
    c2.metric("beta", f"{np.rad2deg(b):.2f} deg")
    c3.metric("gamma", f"{np.rad2deg(g):.2f} deg")
