import streamlit as st

st.set_page_config(
    page_title="Week 5 Project",
    page_icon="🦾",
    layout="wide",
)

st.title("Week 5 Project")

st.markdown(
    """
I built this website to deepen my own understanding of the fundamentals
taught in Week 5 of the NPTEL Robotics course, which is where kinematics
gives way to dynamics: the study of the forces and torques needed to
actually move a robot, not just describe its geometry.

Everything here is built from six lectures' worth of material:

- **Inertia tensors** (Lectures 1-2): deriving the moments of inertia of
  rectangular and circular robot links, and the slender-link approximation.
- **The Lagrange-Euler formulation** (Lectures 2-3): using kinetic and
  potential energy to derive joint torque, including the trace notation
  used to express kinetic energy.
- **The D/h/C term structure** (Lectures 3-5): how the general torque
  equation splits into inertia, Coriolis/centrifugal, and gravity terms
  for a 2-DoF manipulator.
- **The Center of Mass approach** (Lecture 6): a more tractable way to
  derive the same torque equations by hand for a simple 2-DoF or 3-DoF
  robot, which is the method actually implemented here.
    """
)

st.subheader("Pages")
st.markdown(
    """
    1. **Inertia Tensor Calculator** — compute a link's inertia tensor and its center-of-mass value.
    2. **Dynamics Concepts** — forward vs. inverse dynamics, torque components, and the D/h/C structure.
    3. **Kinetic Energy (Trace Notation)** — see why the trace of V*V^T gives kinetic energy.
    4. **2-DoF Joint Torque Calculator** — compute the torques needed to move a 2-link arm, with built-in consistency checks.
    """
)
