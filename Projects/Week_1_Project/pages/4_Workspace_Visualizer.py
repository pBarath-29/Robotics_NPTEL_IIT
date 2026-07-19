import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import streamlit as st
from core.workspace import (
    cartesian_workspace,
    cylindrical_workspace,
    spherical_workspace,
    articulated_workspace,
)

st.set_page_config(page_title="Workspace Visualizer", page_icon="📐", layout="wide")
st.title("📐 Workspace Visualizer")

coord_type = st.selectbox(
    "Coordinate system",
    ["Cartesian", "Cylindrical", "Spherical / Polar", "Revolute / Articulated"],
)

st.divider()

if coord_type == "Cartesian":
    st.markdown("3 independent linear joints (PPP/SSS) → workspace is a **cuboid**.")
    c1, c2, c3 = st.columns(3)
    x_max = c1.slider("X reach (max)", 1, 20, 8)
    y_max = c2.slider("Y reach (max)", 1, 20, 6)
    z_range = c3.slider("Z reach (min, max)", 0, 20, (0, 5))
    fig = cartesian_workspace((0, x_max), (0, y_max), z_range)

elif coord_type == "Cylindrical":
    st.markdown("2 linear joints + 1 twisting joint (TSS/TPP) → workspace is a **cylindrical annulus**.")
    c1, c2 = st.columns(2)
    r_min, r_max = c1.slider("Radial reach (min, max)", 0, 20, (2, 10))
    z_min, z_max = c2.slider("Vertical reach (min, max)", -10, 10, (0, 6))
    fig = cylindrical_workspace(r_min, r_max, z_min, z_max)

elif coord_type == "Spherical / Polar":
    st.markdown("1 linear joint + 2 rotary joints (TRS/TRP) → elevation profile swept by the twisting joint.")
    c1, c2, c3 = st.columns(3)
    r_min, r_max = c1.slider("Radial reach (min, max)", 0, 20, (1, 9))
    elev_min, elev_max = c2.slider("Elevation angle range (deg)", -90, 90, (-30, 60))
    twist = c3.slider("Twist sweep (deg)", 0, 360, 330)
    fig = spherical_workspace(r_min, r_max, elev_min, elev_max, twist)

else:
    st.markdown("3 rotary joints (TRR) → workspace formed by **intersecting partial spheres**, folded and stretched, then swept by the base twist.")
    c1, c2, c3 = st.columns(3)
    r_min, r_max = c1.slider("Reach band (min, max)", 0, 20, (1, 10))
    elev_min, elev_max = c2.slider("Elevation angle range (deg)", -90, 180, (-45, 135))
    twist = c3.slider("Base twist sweep (deg)", 0, 360, 300)
    fig = articulated_workspace(r_min, r_max, elev_min, elev_max, twist)

st.pyplot(fig)

st.info(
    "Reachable workspace: volume the end-effector can reach with **at least "
    "one** orientation. Dextrous workspace: the subset reachable with "
    "**multiple** orientations -- always smaller than the reachable region "
    "(Lecture 4). The dextrous overlay here is a conceptual illustration; "
    "computing it exactly needs forward kinematics, which is beyond Week 1.",
    icon="ℹ️",
)
