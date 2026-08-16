import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import streamlit as st
from core.kinetic_energy import velocity_outer_product, trace_kinetic_energy, direct_kinetic_energy

st.set_page_config(page_title="Kinetic Energy (Trace Notation)", page_icon="🌀", layout="wide")
st.title("🌀 Kinetic Energy (Trace Notation)")

st.markdown(
    """
Squaring a 3D velocity vector as an outer product V*V^T produces a 3x3
matrix. Its diagonal sums to vx^2 + vy^2 + vz^2 -- the Trace. This is why
kinetic energy of a differential mass is written as
dK = (1/2) * Trace(V * V^T) * dm.
"""
)

col1, col2, col3, col4 = st.columns(4)
vx = col1.number_input("vx", value=2.0)
vy = col2.number_input("vy", value=1.0)
vz = col3.number_input("vz", value=0.5)
dm = col4.number_input("dm", min_value=0.0, value=1.0)

outer = velocity_outer_product(vx, vy, vz)
st.subheader("V * V^T")
st.dataframe(outer)

trace_result = trace_kinetic_energy(vx, vy, vz, dm)
direct_result = direct_kinetic_energy(vx, vy, vz, dm)

col5, col6 = st.columns(2)
col5.metric("Trace form: (1/2)*Trace(V V^T)*dm", f"{trace_result:.4f}")
col6.metric("Direct form: (1/2)*dm*(vx^2+vy^2+vz^2)", f"{direct_result:.4f}")

if abs(trace_result - direct_result) < 1e-9:
    st.success("Both forms agree exactly.")
