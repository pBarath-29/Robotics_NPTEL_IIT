import streamlit as st

st.set_page_config(
    page_title="Week 7 Project",
    page_icon="🦾",
    layout="wide",
)

st.title("Week 7 Project")

st.markdown(
    """
I built this website to deepen my own understanding of the fundamentals
taught in Week 7 of the NPTEL Robotics course, which finishes robot
vision and then introduces robot motion planning.

Everything here is built from six lectures' worth of material:

- **Image pre-processing** (Lecture 1): neighborhood averaging and median
  filtering for noise removal, thresholding, and edge detection with
  gradient and Laplacian masks.
- **Boundary descriptors** (Lecture 2): chain codes, signatures, and
  compactness for identifying an object's shape.
- **Motion planning fundamentals** (Lectures 3-4): structured vs.
  unstructured environments, and graph-based path planning algorithms.
- **Dynamic motion planning** (Lecture 5): planning around moving
  obstacles, and the Potential Field Method.
- **Reactive control and evolutionary robotics** (Lecture 6): behaviour-based
  robotics, computational complexity, and biologically inspired approaches.
    """
)

st.subheader("Pages")
st.markdown(
    """
    1. **Image Filters** — apply neighborhood averaging and median filtering to a small image grid.
    2. **Thresholding & Edge Detection** — binarize an image and detect edges with gradient/Laplacian masks.
    3. **Boundary Descriptors** — chain codes, signatures, and compactness-based shape identification.
    4. **Motion Planning Concepts** — a reference for the graph-based and dynamic planning algorithms.
    5. **Potential Field Path Planner** — simulate a robot navigating to a goal around obstacles, including the Local Minima Problem.
    """
)
