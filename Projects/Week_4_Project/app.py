import streamlit as st

st.set_page_config(
    page_title="Week 4 Project",
    page_icon="🦾",
    layout="wide",
)

st.title("Week 4 Project")

st.markdown(
    """
I built this website to deepen my own understanding of the fundamentals
taught in Week 4 of the NPTEL Robotics course, which covers the forward
and inverse kinematics of a 5-DoF manipulator, more Denavit-Hartenberg
examples, trajectory planning, and Jacobians and singularities.

Everything here is built from six lectures' worth of material:

- **Forward kinematics of a 5-DoF manipulator** (Lecture 1): the MINIMOVER
  case study, built from its DH table and checked against the closed-form
  position equations given in the notes.
- **Inverse kinematics of a 5-DoF manipulator** (Lecture 2): solving for
  all five joint angles from a target position and orientation.
- **More DH parameter examples** (Lecture 3): the T-S-R and S-T-R
  3-DoF manipulators.
- **Trajectory planning** (Lectures 4-5): cubic and quintic polynomials,
  and linear trajectories with parabolic blends.
- **Jacobians and singularities** (Lecture 6): detecting when a 2-DoF arm
  loses a degree of freedom.
    """
)

st.subheader("Pages")
st.markdown(
    """
    1. **MINIMOVER Forward Kinematics** — compute the end-effector pose from joint angles.
    2. **MINIMOVER Inverse Kinematics** — solve for the joint angles that reach a target pose.
    3. **DH Examples (T-S-R / S-T-R)** — browse two more worked DH parameter assignments.
    4. **Trajectory Planning** — fit cubic, quintic, or parabolic-blend trajectories.
    5. **Jacobian & Singularity** — check a 2-DoF arm pose for singularities.
    """
)
