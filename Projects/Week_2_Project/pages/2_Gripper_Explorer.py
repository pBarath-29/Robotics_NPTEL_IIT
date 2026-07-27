import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import streamlit as st
from core.grippers import (
    CLASSIFICATION_AXES,
    MECHANICAL_DESIGNS,
    SPECIALIZED_GRIPPERS,
    RCC_PEG_IN_HOLE,
)

st.set_page_config(page_title="Gripper Explorer", page_icon="🤖", layout="wide")
st.title("🤖 Gripper Explorer")

tab1, tab2, tab3, tab4 = st.tabs([
    "Classification", "Mechanical Designs", "Specialized Grippers", "RCC Peg-in-Hole",
])

with tab1:
    st.subheader("Four ways to classify a gripper")
    for axis, options in CLASSIFICATION_AXES.items():
        st.markdown(f"**{axis}**")
        for name, desc in options.items():
            st.markdown(f"- **{name}**: {desc}")

with tab2:
    st.subheader("Simple mechanical gripper designs")
    st.caption("These are cost-effective but less versatile designs, usually driven by a sliding piston-cylinder.")
    for name, desc in MECHANICAL_DESIGNS.items():
        st.markdown(f"**{name}**: {desc}")

with tab3:
    st.subheader("Specialized grippers")
    for name, info in SPECIALIZED_GRIPPERS.items():
        with st.expander(name):
            st.markdown(f"**Description:** {info['description']}")
            st.markdown(f"**Drawback:** {info['drawback']}")
            st.markdown(f"**Ungripping:** {info['ungripping']}")

with tab4:
    st.subheader("The peg-in-hole insertion problem")
    st.markdown(f"**Lateral error:** {RCC_PEG_IN_HOLE['lateral_error']}")
    st.markdown(f"**Angular error:** {RCC_PEG_IN_HOLE['angular_error']}")
    st.markdown(f"**Solution:** {RCC_PEG_IN_HOLE['solution']}")
