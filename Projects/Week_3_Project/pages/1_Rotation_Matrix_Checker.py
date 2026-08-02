import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import numpy as np
import streamlit as st
from core.rotations import compose_rotations, check_rotation_properties

st.set_page_config(page_title="Rotation Matrix Checker", page_icon="🔄", layout="wide")
st.title("🔄 Rotation Matrix Checker")

st.markdown(
    """
A valid 3x3 rotation matrix must have unit-length rows and columns, have
every distinct pair of rows (and columns) orthogonal to each other, and
have an inverse equal to its transpose. Build a matrix from a sequence of
rotations, or enter your own, and check whether it holds up.
"""
)

mode = st.radio("How do you want to provide a matrix?", ["Build from a rotation sequence", "Enter a custom matrix"])

if mode == "Build from a rotation sequence":
    st.caption(
        "Rotations are multiplied right-to-left: the first one you list "
        "ends up at the far right of the matrix product."
    )
    num_steps = st.number_input("Number of rotations in the sequence", min_value=1, max_value=5, value=3, step=1)
    sequence = []
    for i in range(int(num_steps)):
        col1, col2 = st.columns(2)
        axis = col1.selectbox(f"Step {i+1} axis", ["X", "Y", "Z"], key=f"axis_{i}")
        angle_deg = col2.number_input(f"Step {i+1} angle (degrees)", value=30.0, key=f"angle_{i}")
        sequence.append((axis, np.deg2rad(angle_deg)))
    matrix = compose_rotations(sequence)
else:
    st.caption("Enter each element of the 3x3 matrix.")
    matrix = np.zeros((3, 3))
    default = np.eye(3)
    for i in range(3):
        cols = st.columns(3)
        for j in range(3):
            matrix[i, j] = cols[j].number_input(f"r[{i+1}][{j+1}]", value=float(default[i, j]), key=f"m_{i}_{j}")

st.subheader("Matrix")
st.dataframe(matrix)

result = check_rotation_properties(matrix)

col1, col2, col3 = st.columns(3)
col1.metric("Unit vectors", "Yes" if result["unit_vectors"] else "No")
col2.metric("Orthogonal", "Yes" if result["orthogonal"] else "No")
col3.metric("Inverse = Transpose", "Yes" if result["inverse_equals_transpose"] else "No")

st.markdown("**Row norms:** " + ", ".join(f"{n:.4f}" for n in result["row_norms"]))
st.markdown("**Column norms:** " + ", ".join(f"{n:.4f}" for n in result["col_norms"]))

if result["is_valid_rotation"]:
    st.success("This is a valid rotation matrix.")
else:
    st.error("This is not a valid rotation matrix.")
