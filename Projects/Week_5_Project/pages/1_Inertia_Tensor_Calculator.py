import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import streamlit as st
from core.inertia import (
    rectangular_inertia_tensor,
    circular_inertia_tensor,
    circular_center_of_mass_izz,
    rectangular_center_of_mass_izz,
)

st.set_page_config(page_title="Inertia Tensor Calculator", page_icon="🧱", layout="wide")
st.title("🧱 Inertia Tensor Calculator")

st.markdown(
    "Compute the inertia tensor of a robot link, with the coordinate frame "
    "at the motor end (not the center of mass), matching how dynamic "
    "control calculations are set up."
)

shape = st.radio("Link shape", ["Rectangular", "Circular"])

col1, col2, col3 = st.columns(3)
m = col1.number_input("Mass m", min_value=0.01, value=2.0)
l = col2.number_input("Length l", min_value=0.01, value=1.0)

if shape == "Rectangular":
    b = col3.number_input("Cross-section side b", min_value=0.0, value=0.1)
    a = st.number_input("Cross-section side a", min_value=0.0, value=0.1)
    slender = st.checkbox("Apply the slender-link approximation (a, b -> 0)")
    if slender:
        a = b = 0.0
    tensor = rectangular_inertia_tensor(m, a, b, l)
    com_izz = rectangular_center_of_mass_izz(m, a, l)
else:
    r = col3.number_input("Radius r", min_value=0.0, value=0.1)
    slender = st.checkbox("Apply the slender-link approximation (r -> 0)")
    if slender:
        r = 0.0
    tensor = circular_inertia_tensor(m, r, l)
    com_izz = circular_center_of_mass_izz(m, r, l)

st.divider()
st.subheader("Inertia tensor (motor-end frame)")
c1, c2, c3 = st.columns(3)
c1.metric("Ixx", f"{tensor.ixx:.5f}")
c2.metric("Iyy", f"{tensor.iyy:.5f}")
c3.metric("Izz", f"{tensor.izz:.5f}")
st.caption("All products of inertia (Ixy, Iyz, Izx) are 0 for a symmetric link.")
st.markdown(f"**Center of mass:** {tensor.center_of_mass}")

st.subheader("Izz shifted to the center of mass (Parallel Axis Theorem)")
st.metric("Izz (center of mass)", f"{com_izz:.5f}")
if shape == "Circular":
    st.caption("Closed-form check from Lecture 6: Izz(c) = (1/12)*m*l^2 + (1/4)*m*r^2.")
