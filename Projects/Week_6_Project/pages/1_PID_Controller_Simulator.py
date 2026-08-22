import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import matplotlib.pyplot as plt
import streamlit as st
from core.control import simulate_step_response

st.set_page_config(page_title="PID Controller Simulator", page_icon="🎛️", layout="wide")
st.title("🎛️ PID Controller Simulator")

st.markdown(
    """
Partitioned control chooses tau = alpha*tau' + beta so that alpha and beta
exactly cancel the robot's true dynamics, leaving a plain double
integrator theta'' = tau'. That's why the PID law is written directly in
terms of the desired acceleration, error, and error derivative: it turns
the closed loop into a simple, tunable second-order system,
E'' + Kd*E' + Kp*E (+ Ki*integral(E)) = 0.

Tune the gains below and watch a single joint track a constant target
angle (a step response) from a different starting angle.
"""
)

col1, col2 = st.columns(2)
theta0 = col1.number_input("Starting angle theta0 (deg)", value=0.0)
theta_d = col2.number_input("Target angle theta_d (deg)", value=90.0)

col3, col4, col5 = st.columns(3)
kp = col3.number_input("Kp", min_value=0.0, value=25.0)
kd = col4.number_input("Kd", min_value=0.0, value=8.0)
ki = col5.number_input("Ki (0 for pure PD)", min_value=0.0, value=0.0)

col6, col7 = st.columns(2)
t_final = col6.number_input("Simulation time (s)", min_value=0.1, value=5.0)
dt = col7.number_input("Time step dt (s)", min_value=0.0001, value=0.01, format="%.4f")

t, theta, error = simulate_step_response(theta_d, theta0, kp, kd, ki, dt, t_final)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4))
ax1.plot(t, theta, label="theta(t)")
ax1.axhline(theta_d, color="tab:red", linestyle="--", label="theta_d")
ax1.set_xlabel("t (s)")
ax1.set_ylabel("angle (deg)")
ax1.set_title("Joint angle")
ax1.legend()
ax1.grid(True, linestyle="--", alpha=0.4)

ax2.plot(t, error, color="tab:orange")
ax2.set_xlabel("t (s)")
ax2.set_ylabel("error (deg)")
ax2.set_title("Tracking error")
ax2.grid(True, linestyle="--", alpha=0.4)

fig.tight_layout()
st.pyplot(fig)

final_error = error[-1]
st.metric("Final error", f"{final_error:.4f} deg")
if abs(final_error) < 0.5:
    st.success("The controller converged to the target angle.")
else:
    st.warning("The controller has not converged -- try increasing Kp or Kd, or simulating for longer.")
