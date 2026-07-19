import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import streamlit as st
from core.grubler import compute_mobility, classify_mobility, WORKED_EXAMPLES

st.set_page_config(page_title="Grubler Calculator", page_icon="🧮", layout="wide")
st.title("🧮 Grubler's Criterion Calculator")

st.markdown(
    """
    - **Planar** manipulators use lambda = 3.
    - **Spatial** (3D) manipulators use lambda = 6.
    - `n` = number of *moving* links (the fixed base is not counted).
    - `Ci` = connectivity (DoF) of joint *i*.
    """
)

if "n_value" not in st.session_state:
    st.session_state.n_value = 4
if "ci_text" not in st.session_state:
    st.session_state.ci_text = "1,1,1,1"
if "spatial" not in st.session_state:
    st.session_state.spatial = False

st.subheader("Load a worked example from the notes")
example_cols = st.columns(len(WORKED_EXAMPLES))
for col, (name, data) in zip(example_cols, WORKED_EXAMPLES.items()):
    if col.button(name):
        st.session_state.n_value = data["n"]
        st.session_state.ci_text = ",".join(str(c) for c in data["joint_dofs"])
        st.session_state.spatial = data["spatial"]

st.divider()

spatial = st.radio(
    "Manipulator type",
    options=[False, True],
    format_func=lambda s: "Spatial (3D, lambda = 6)" if s else "Planar (2D, lambda = 3)",
    index=1 if st.session_state.spatial else 0,
)
n = st.number_input("Number of moving links (n)", min_value=1, value=st.session_state.n_value, step=1)
ci_text = st.text_input(
    "Joint connectivities (Ci), comma-separated -- one value per joint",
    value=st.session_state.ci_text,
)

try:
    joint_dofs = [int(x.strip()) for x in ci_text.split(",") if x.strip()]
    valid = len(joint_dofs) > 0 and all(1 <= c <= 6 for c in joint_dofs)
except ValueError:
    joint_dofs = []
    valid = False

if not valid:
    st.error("Enter a comma-separated list of joint DoF values, e.g. 1,1,1,1 (each between 1 and 6).")
else:
    result = compute_mobility(n=int(n), joint_dofs=joint_dofs, spatial=spatial)
    classification = classify_mobility(result.mobility, spatial)

    col1, col2, col3 = st.columns(3)
    col1.metric("Mobility (M)", result.mobility)
    col2.metric("Number of joints (m)", len(joint_dofs))
    col3.metric("Classification", classification)

    lam = result.lam
    constraint_terms = " + ".join(f"({lam}-{c})" for c in joint_dofs)
    st.latex(
        rf"M = {lam} \times {int(n)} - [{constraint_terms}] = {lam*int(n)} - {sum(lam - c for c in joint_dofs)} = {result.mobility}"
    )

    required = 6 if spatial else 3
    if classification == "Ideal":
        st.success(f"M = {result.mobility} matches the required DoF ({required}) exactly -- an ideal manipulator.")
    elif classification == "Redundant":
        st.warning(f"M = {result.mobility} exceeds the required DoF ({required}) -- a redundant manipulator, useful for reaching constrained spaces (e.g. welding in tight geometry).")
    else:
        st.warning(f"M = {result.mobility} is less than the required DoF ({required}) -- an under-actuated manipulator, suited to tasks like simple pick-and-place where full orientation control isn't needed.")
