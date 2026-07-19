import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import streamlit as st
from core.joints import JOINTS, joint_symbols

st.set_page_config(page_title="Joint Explorer", page_icon="🔩", layout="wide")
st.title("🔩 Joint Explorer")

symbol = st.selectbox(
    "Choose a joint symbol",
    joint_symbols(),
    format_func=lambda s: f"{s} — {JOINTS[s]['name']}",
)

joint = JOINTS[symbol]

col1, col2 = st.columns([1, 2])
with col1:
    st.metric("Degrees of Freedom", joint["dof"])
    st.metric("Category", joint["category"])
with col2:
    st.subheader(f"{symbol} — {joint['name']}")
    st.write(joint["description"])
    st.markdown(f"**Real-world analogy:** {joint['analogy']}")

st.divider()
st.subheader("All joint types at a glance")

import pandas as pd

df = pd.DataFrame([
    {"Symbol": s, "Name": j["name"], "Category": j["category"], "DoF": j["dof"]}
    for s, j in JOINTS.items()
])
st.dataframe(df, use_container_width=True, hide_index=True)

st.markdown(
    """
    **Note:** Cylindrical (C) and Hooke/Universal (U) joints each provide
    2 DoF; the Spherical joint (S') provides 3 DoF. All others are 1-DoF
    joints. (Lecture 2, "Robotic Joints & Degrees of Freedom")
    """
)
