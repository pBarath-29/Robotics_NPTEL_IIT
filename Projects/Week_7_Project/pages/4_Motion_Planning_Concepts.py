import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import streamlit as st
from core.motion_planning_reference import (
    MOTION_PLANNING_TYPES,
    PROBLEM_TYPES,
    ENVIRONMENT_TYPES,
    GRAPH_BASED_ALGORITHMS,
    DYNAMIC_PLANNING_METHODS,
    COMPLEXITY_CLASSES,
    REACTIVE_CONTROL,
    EVOLUTIONARY_ROBOTICS,
)

st.set_page_config(page_title="Motion Planning Concepts", page_icon="🗺️", layout="wide")
st.title("🗺️ Motion Planning Concepts")

st.subheader("Types of motion planning")
for name, desc in MOTION_PLANNING_TYPES.items():
    st.markdown(f"**{name}**: {desc}")

st.subheader("Manipulation vs. navigation")
for name, desc in PROBLEM_TYPES.items():
    st.markdown(f"**{name}**: {desc}")

st.subheader("Structured vs. unstructured environments")
for name, desc in ENVIRONMENT_TYPES.items():
    st.markdown(f"**{name}**: {desc}")

st.divider()
st.subheader("Graph-based algorithms (static, structured environments)")
for name, info in GRAPH_BASED_ALGORITHMS.items():
    with st.expander(f"{name} ({info['proposer']})"):
        st.write(info["summary"])

st.divider()
st.subheader("Dynamic motion planning methods")
for name, info in DYNAMIC_PLANNING_METHODS.items():
    with st.expander(f"{name} ({info['proposer']})"):
        st.write(info["summary"])

st.divider()
st.subheader("Computational complexity")
for name, desc in COMPLEXITY_CLASSES.items():
    st.markdown(f"**{name}**: {desc}")

st.divider()
st.subheader(f"Reactive control ({REACTIVE_CONTROL['proposer']})")
st.write(REACTIVE_CONTROL["summary"])
for drawback in REACTIVE_CONTROL["drawbacks"]:
    st.markdown(f"- {drawback}")

st.divider()
st.subheader("Evolutionary robotics")
for name, desc in EVOLUTIONARY_ROBOTICS.items():
    st.markdown(f"**{name}**: {desc}")
