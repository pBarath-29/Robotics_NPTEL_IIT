import streamlit as st

st.set_page_config(
    page_title="Week 1 Project",
    page_icon="🦾",
    layout="wide",
)

st.title("Week 1 Project")

st.markdown(
    """
I built this website to deepen my own understanding of the fundamentals
taught in Week 1, "Introduction to Robots and Robotics," of the NPTEL
Robotics course.

Everything here is built from five lectures' worth of material:

- **Joint types & DoF** (Lectures 1-3): Revolute, Prismatic, Sliding,
  Twisting, Cylindrical, Hooke/Universal, Spherical joints.
- **Grubler's Criterion** (Lectures 3-4): computing manipulator mobility
  and classifying it as ideal / redundant / under-actuated.
- **Robot classification** (Lecture 4): task type, controller type, and
  coordinate-system taxonomy (Cartesian, Cylindrical, Spherical,
  Articulated) with real named industrial robots.
- **Workspace geometry** (Lectures 4-5): reachable vs. dextrous workspace,
  visualized via 2D elevation/plan-view cross-sections -- the same
  simplification the lecture itself uses for 3D workspaces.
- **Performance specifications** (Lecture 5): resolution (BRU, control
  resolution from encoder pulses), accuracy, and repeatability.
    """
)

st.subheader("Pages")
st.markdown(
    """
    1. **Joint Explorer** — look up any joint symbol's DoF and behavior.
    2. **Grubler Calculator** — compute manipulator mobility and verify
       against the lecture's worked examples.
    3. **Robot Classifier** — identify a manipulator's coordinate system
       from its joint sequence.
    4. **Workspace Visualizer** — see the reachable workspace shape for
       each coordinate system.
    5. **Performance Specs** — resolution, accuracy, and repeatability
       calculators.
    """
)
