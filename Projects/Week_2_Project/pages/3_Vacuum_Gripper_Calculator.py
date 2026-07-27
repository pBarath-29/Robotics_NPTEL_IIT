import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import streamlit as st
from core.vacuum_gripper import (
    AIR_DENSITY_KG_M3,
    GRAVITY_M_S2,
    throat_velocity,
    pressure_drop,
    lift_force,
    can_hold,
)

st.set_page_config(page_title="Vacuum Gripper Calculator", page_icon="🧲", layout="wide")
st.title("🧲 Vacuum Gripper Calculator")

st.markdown(
    """
Air forced through an orifice into a narrower venturi throat speeds up
(continuity equation), and as its velocity increases, its pressure drops
(Bernoulli's equation). That pressure drop, compared to atmospheric
pressure outside, is what holds a flat object against the cup.
"""
)

col1, col2 = st.columns(2)
with col1:
    inlet_velocity = st.slider("Inlet air velocity (m/s)", 1.0, 50.0, 10.0, 0.5)
    inlet_area_cm2 = st.slider("Inlet area (cm^2)", 1.0, 20.0, 8.0, 0.5)
    throat_area_cm2 = st.slider("Throat area (cm^2)", 0.5, inlet_area_cm2, 2.0, 0.5)
with col2:
    cup_area_cm2 = st.slider("Cup contact area (cm^2)", 1.0, 100.0, 30.0, 1.0)
    object_mass_kg = st.slider("Object mass (kg)", 0.1, 20.0, 2.0, 0.1)

inlet_area_m2 = inlet_area_cm2 * 1e-4
throat_area_m2 = throat_area_cm2 * 1e-4
cup_area_m2 = cup_area_cm2 * 1e-4

v_throat = throat_velocity(inlet_velocity, inlet_area_m2, throat_area_m2)
drop = pressure_drop(inlet_velocity, v_throat)
force = lift_force(drop, cup_area_m2)
weight = object_mass_kg * GRAVITY_M_S2
holds = can_hold(force, object_mass_kg)

col3, col4, col5 = st.columns(3)
col3.metric("Throat velocity", f"{v_throat:.2f} m/s")
col4.metric("Pressure drop", f"{drop:.1f} Pa")
col5.metric("Lift force", f"{force:.2f} N")

st.markdown(f"Object weight: **{weight:.2f} N**")

if holds:
    st.success(f"The vacuum gripper can hold this object (lift force {force:.2f} N >= weight {weight:.2f} N).")
else:
    st.error(f"The vacuum gripper cannot hold this object (lift force {force:.2f} N < weight {weight:.2f} N). Try a larger cup area or a smaller throat.")

st.caption(f"Air density used: {AIR_DENSITY_KG_M3} kg/m^3 (standard air at sea level).")
