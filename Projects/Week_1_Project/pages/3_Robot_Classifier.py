import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import streamlit as st
from core.classification import (
    COORDINATE_SYSTEMS,
    TASK_TYPES,
    CONTROLLER_TYPES,
    classify_sequence,
)

st.set_page_config(page_title="Robot Classifier", page_icon="🏷️", layout="wide")
st.title("🏷️ Robot Classifier")

st.subheader("1. Classify by joint sequence")
st.markdown(
    "Enter a 3-letter joint sequence for a serial manipulator "
    "(e.g. `PPP`, `SSS`, `TSS`, `TPP`, `TRS`, `TRP`, `TRR`)."
)

sequence = st.text_input("Joint sequence", value="TRR").strip().upper()

system, data = classify_sequence(sequence)

if system is None:
    st.error(
        f"'{sequence}' doesn't match any coordinate-system pattern covered "
        f"in Week 1: PPP/SSS (Cartesian), TSS/TPP (Cylindrical), "
        f"TRS/TRP (Spherical), TRR (Articulated)."
    )
else:
    st.success(f"**{system}** manipulator")
    col1, col2 = st.columns([2, 1])
    with col1:
        st.write(data["description"])
        st.markdown(f"**Workspace shape:** {data['workspace_shape']}")
    with col2:
        st.markdown("**Real-world examples:**")
        for ex in data["examples"]:
            st.markdown(f"- {ex}")

st.divider()
st.subheader("2. Coordinate-system reference table")
for name, d in COORDINATE_SYSTEMS.items():
    with st.expander(f"{name}  ({' / '.join(d['patterns'])})"):
        st.write(d["description"])
        st.markdown(f"**Workspace shape:** {d['workspace_shape']}")
        st.markdown(f"**Examples:** {', '.join(d['examples'])}")

st.divider()
st.subheader("3. Task type")
for name, desc in TASK_TYPES.items():
    st.markdown(f"**{name}** — {desc}")

st.subheader("4. Controller type")
for name, desc in CONTROLLER_TYPES.items():
    st.markdown(f"**{name}** — {desc}")
