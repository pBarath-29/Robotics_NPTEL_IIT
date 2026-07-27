import streamlit as st

st.set_page_config(
    page_title="Week 2 Project",
    page_icon="🦾",
    layout="wide",
)

st.title("Week 2 Project")

st.markdown(
    """
I built this website to deepen my own understanding of the fundamentals
taught in Week 2 of the NPTEL Robotics course, which covers applications of
robotics, end-effectors and grippers, robot teaching methods, economic
analysis of a robot purchase, and the basics of frame transformations.

Everything here is built from seven lectures' worth of material:

- **Applications of robotics** (Lecture 1): manufacturing, underwater,
  medical, space, and agricultural applications.
- **End-effectors and grippers** (Lectures 2-3): classification, mechanical
  gripper designs, vacuum grippers, and specialized grippers.
- **Robot teaching methods** (Lectures 3-4): online and offline teaching,
  and the VAL programming language.
- **Economic analysis** (Lectures 4-5): the formulas used to decide if a
  robot purchase is financially worth it, checked against a worked case
  study from the notes.
- **Frame transformations** (Lectures 6-7): representing position and
  orientation, and composing translation and rotation operators into a
  single transformation.
    """
)

st.subheader("Pages")
st.markdown(
    """
    1. **Applications Explorer** — browse robotics applications by domain.
    2. **Gripper Explorer** — look up gripper classifications and designs.
    3. **Vacuum Gripper Calculator** — calculate the lift force of a vacuum gripper.
    4. **Teaching & VAL** — compare teaching methods and build a VAL pick-and-place program.
    5. **Economic Analysis** — work out whether a robot purchase pays off.
    6. **Frame Transformation** — compose translation and rotation operators and apply them to a point.
    """
)
