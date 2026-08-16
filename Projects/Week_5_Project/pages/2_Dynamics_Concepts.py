import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import streamlit as st
from core.dynamics_reference import (
    DYNAMICS_TYPES,
    TORQUE_COMPONENTS,
    DH_TERM_STRUCTURE,
    NOTABLE_FACTS_2DOF,
)

st.set_page_config(page_title="Dynamics Concepts", page_icon="📚", layout="wide")
st.title("📚 Dynamics Concepts")

st.subheader("Forward vs. Inverse Dynamics")
for name, desc in DYNAMICS_TYPES.items():
    st.markdown(f"**{name}**: {desc}")

st.divider()
st.subheader("Components of joint torque")
for name, desc in TORQUE_COMPONENTS.items():
    st.markdown(f"**{name}**: {desc}")

st.divider()
st.subheader("Structure of the Lagrange-Euler torque terms")
st.markdown("tau_i = (d/dt)[dL/d(theta_i')] - dL/d(theta_i), where L = K - P.")
for name, formula in DH_TERM_STRUCTURE.items():
    st.markdown(f"**{name}**")
    st.code(formula, language="text")

st.divider()
st.subheader("Notable facts for the 2-DoF case study")
for fact in NOTABLE_FACTS_2DOF:
    st.markdown(f"- {fact}")
