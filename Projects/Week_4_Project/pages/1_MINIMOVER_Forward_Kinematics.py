import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import numpy as np
import streamlit as st
from core.minimover_fk import compute, closed_form_position

st.set_page_config(page_title="MINIMOVER Forward Kinematics", page_icon="🦾", layout="wide")
st.title("🦾 MINIMOVER Forward Kinematics")

st.markdown(
    "The MINIMOVER is a 5-DoF spatial manipulator with joint configuration "
    "T-R-R-R-T. Enter the link lengths and joint angles to compute the "
    "end-effector's position and orientation."
)

col1, col2 = st.columns(2)
l1 = col1.number_input("L1", min_value=0.0, value=2.0)
l2 = col2.number_input("L2", min_value=0.0, value=1.5)

cols = st.columns(5)
thetas_deg = [cols[i].number_input(f"theta{i+1} (deg)", value=10.0 * (i + 1), key=f"t_{i}") for i in range(5)]
thetas = [np.deg2rad(t) for t in thetas_deg]

t_final, frames = compute(l1, l2, thetas)
position = t_final[:3, 3]

st.divider()
st.subheader("Final transformation matrix (T_5_0)")
st.dataframe(t_final)

st.subheader("End-effector position")
c1, c2, c3 = st.columns(3)
c1.metric("x", f"{position[0]:.4f}")
c2.metric("y", f"{position[1]:.4f}")
c3.metric("z", f"{position[2]:.4f}")

expected = closed_form_position(l1, l2, thetas[0], thetas[1], thetas[2])
st.caption(
    f"Closed-form check from the notes (depends only on theta1-3): "
    f"expected ({expected[0]:.4f}, {expected[1]:.4f}, {expected[2]:.4f})."
)
