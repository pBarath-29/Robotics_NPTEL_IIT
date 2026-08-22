import streamlit as st

st.set_page_config(
    page_title="Week 6 Project",
    page_icon="🦾",
    layout="wide",
)

st.title("Week 6 Project")

st.markdown(
    """
I built this website to deepen my own understanding of the fundamentals
taught in Week 6 of the NPTEL Robotics course, which covers how a robot
actually senses and controls itself: control schemes, the sensors that
feed them, and the beginnings of robot vision.

Everything here is built from five lectures' worth of material:

- **Control schemes** (Lecture 1): partitioned control and PD/PID joint
  control laws.
- **Sensors** (Lectures 2-4): classification, position sensors
  (potentiometers, encoders), force/moment sensors, and range/proximity
  sensors.
- **Robot vision** (Lecture 5): frame grabbing and image pre-processing
  with masking.
    """
)

st.subheader("Pages")
st.markdown(
    """
    1. **PID Controller Simulator** — tune a PD/PID joint controller and watch it track a target angle.
    2. **Sensor Classification** — browse how sensors are classified and specified.
    3. **Encoders** — compute absolute encoder resolution and incremental encoder direction.
    4. **Potentiometer & Force Sensor** — voltage-divider and wrist force/moment sensor calculators.
    5. **Range & Proximity Sensors** — triangulation distance calculator and a proximity sensor reference.
    6. **Image Masking** — apply a 3x3 convolution mask to a small image grid.
    """
)
