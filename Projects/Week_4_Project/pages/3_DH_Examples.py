import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import numpy as np
import streamlit as st
from core.dh import forward_kinematics
from core.dh_examples import DH_EXAMPLES, build_numeric_dh_table

st.set_page_config(page_title="DH Examples", page_icon="📋", layout="wide")
st.title("📋 DH Examples: T-S-R and S-T-R")

example_name = st.selectbox("Choose an example", list(DH_EXAMPLES.keys()))
example = DH_EXAMPLES[example_name]
st.markdown(example["description"])

st.subheader("DH parameter table")
for row in example["rows"]:
    theta_str = "Variable" if row["theta_variable"] else f"{row['theta_fixed_deg']} deg (fixed)"
    d_str = "Variable" if row["d_variable"] else f"{row['d_fixed']}"
    st.markdown(
        f"**Frame {row['name']}** -- theta: {theta_str}, d: {d_str}, "
        f"alpha: {row['alpha_deg']} deg, a: {row['a']}"
    )

st.divider()
st.subheader("Try it with numbers")

theta_values_deg = {}
d_values = {}
for i, row in enumerate(example["rows"]):
    cols = st.columns(2)
    if row["theta_variable"]:
        theta_values_deg[i] = cols[0].number_input(f"Frame {row['name']} theta (deg)", value=20.0, key=f"dh_theta_{i}")
    if row["d_variable"]:
        d_values[i] = cols[1].number_input(f"Frame {row['name']} d", value=5.0, key=f"dh_d_{i}")

a_c_value = st.number_input("Link dimension c (final link length)", min_value=0.0, value=3.0)

dh_table = build_numeric_dh_table(example_name, theta_values_deg, d_values, a_c_value)
t_final, _ = forward_kinematics(dh_table)
position = t_final[:3, 3]

st.subheader("End-effector position")
c1, c2, c3 = st.columns(3)
c1.metric("x", f"{position[0]:.4f}")
c2.metric("y", f"{position[1]:.4f}")
c3.metric("z", f"{position[2]:.4f}")
