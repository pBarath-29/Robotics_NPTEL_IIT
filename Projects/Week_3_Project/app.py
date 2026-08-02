import streamlit as st

st.set_page_config(
    page_title="Week 3 Project",
    page_icon="🦾",
    layout="wide",
)

st.title("Week 3 Project")

st.markdown(
    """
I built this website to deepen my own understanding of the fundamentals
taught in Week 3 of the NPTEL Robotics course, which is where the actual
kinematics starts: rotation matrices, coordinate transformations,
orientation representations, Denavit-Hartenberg notation, and forward and
inverse kinematics.

Everything here is built from five lectures' worth of material:

- **Rotation matrices and coordinate transformations** (Lecture 1): the
  properties every valid rotation matrix must satisfy, the composite
  rotation rule, and cylindrical/spherical coordinate mapping.
- **Orientation representations** (Lecture 2): Roll-Pitch-Yaw and Euler
  angles, and converting between an orientation matrix and its angles.
- **Denavit-Hartenberg notation** (Lecture 3): the four DH parameters and
  the rules for assigning coordinate frames to a serial manipulator.
- **Forward kinematics** (Lecture 4): building the transformation matrix
  from the DH parameters and solving a 2-DoF planar arm as a worked case.
- **Inverse kinematics** (Lecture 5): solving for the joint angles needed
  to reach a target point, plus a 5-DoF DH case study.
    """
)

st.subheader("Pages")
st.markdown(
    """
    1. **Rotation Matrix Checker** — verify whether a matrix is a valid rotation matrix.
    2. **Coordinate Converter** — convert cylindrical or spherical coordinates to Cartesian.
    3. **RPY & Euler Angles** — build or extract an orientation from Roll-Pitch-Yaw or Euler angles.
    4. **DH Forward Kinematics** — build a Denavit-Hartenberg table and compute the end-effector pose.
    5. **Inverse Kinematics** — solve the joint angles for a 2-DoF planar arm to reach a target point.
    """
)
