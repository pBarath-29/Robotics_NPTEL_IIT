import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import numpy as np
import streamlit as st
from core.coordinates import cylindrical_to_cartesian, spherical_to_cartesian

st.set_page_config(page_title="Coordinate Converter", page_icon="🧭", layout="wide")
st.title("🧭 Coordinate Converter")

tab1, tab2 = st.tabs(["Cylindrical", "Spherical"])

with tab1:
    st.markdown("Sequence: translate along X by r, rotate about Z by theta, translate along Z by z.")
    col1, col2, col3 = st.columns(3)
    r = col1.number_input("r", min_value=0.0, value=5.0, key="cyl_r")
    theta_deg = col2.number_input("theta (degrees)", value=45.0, key="cyl_theta")
    z = col3.number_input("z", value=2.0, key="cyl_z")
    qx, qy, qz = cylindrical_to_cartesian(r, np.deg2rad(theta_deg), z)
    c1, c2, c3 = st.columns(3)
    c1.metric("qx", f"{qx:.4f}")
    c2.metric("qy", f"{qy:.4f}")
    c3.metric("qz", f"{qz:.4f}")

with tab2:
    st.markdown("Sequence: translate along Z by r, rotate about Y by alpha, rotate about Z by beta.")
    col1, col2, col3 = st.columns(3)
    r_s = col1.number_input("r", min_value=0.0, value=5.0, key="sph_r")
    alpha_deg = col2.number_input("alpha (degrees)", value=60.0, key="sph_alpha")
    beta_deg = col3.number_input("beta (degrees)", value=45.0, key="sph_beta")
    qx2, qy2, qz2 = spherical_to_cartesian(r_s, np.deg2rad(alpha_deg), np.deg2rad(beta_deg))
    c4, c5, c6 = st.columns(3)
    c4.metric("qx", f"{qx2:.4f}")
    c5.metric("qy", f"{qy2:.4f}")
    c6.metric("qz", f"{qz2:.4f}")
