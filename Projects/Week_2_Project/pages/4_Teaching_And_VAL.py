import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import streamlit as st
from core.teaching import (
    ONLINE_METHODS,
    OFFLINE_METHODS,
    VAL_OTHER_COMMANDS,
    build_pick_and_place,
)

st.set_page_config(page_title="Teaching & VAL", page_icon="🕹️", layout="wide")
st.title("🕹️ Teaching & VAL")

tab1, tab2 = st.tabs(["Teaching Methods", "VAL Pick-and-Place Builder"])

with tab1:
    st.subheader("Online teaching")
    st.caption("Uses the physical robot itself to record instructions.")
    for name, desc in ONLINE_METHODS.items():
        st.markdown(f"**{name}**: {desc}")

    st.subheader("Offline teaching")
    st.caption("Does not use the physical robot during programming.")
    for name, desc in OFFLINE_METHODS.items():
        st.markdown(f"**{name}**: {desc}")

with tab2:
    st.markdown(
        "Fill in the pick-and-place parameters and see the resulting VAL "
        "program, using the exact command sequence from the notes."
    )
    col1, col2 = st.columns(2)
    with col1:
        part = st.text_input("Part name", value="PART")
        bin_name = st.text_input("Bin name", value="BIN")
        approach_mm = st.number_input("Approach height above part (mm)", min_value=1, value=100)
    with col2:
        depart1_mm = st.number_input("Depart distance after grasp (mm)", min_value=1, value=200)
        bin_approach_mm = st.number_input("Approach height above bin (mm)", min_value=1, value=300)
        depart2_mm = st.number_input("Depart distance after release (mm)", min_value=1, value=100)

    program = build_pick_and_place(
        part=part, bin_name=bin_name, approach_mm=approach_mm,
        depart1_mm=depart1_mm, bin_approach_mm=bin_approach_mm, depart2_mm=depart2_mm,
    )
    st.code(program, language="text")

    st.subheader("Other VAL commands")
    for cmd, desc in VAL_OTHER_COMMANDS.items():
        st.markdown(f"**{cmd}**: {desc}")

    st.info(
        "Teaching and programming only provide instructions to the robot; "
        "they do not by themselves make the robot intelligent.",
        icon="ℹ️",
    )
