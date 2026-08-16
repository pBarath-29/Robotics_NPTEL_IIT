import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from core.trajectory import cubic_coeffs, quintic_coeffs, poly_eval, parabolic_blend

st.set_page_config(page_title="Trajectory Planning", page_icon="📈", layout="wide")
st.title("📈 Trajectory Planning")

tab1, tab2, tab3 = st.tabs(["Cubic Polynomial", "Quintic Polynomial", "Linear with Parabolic Blends"])


def plot_trajectory(coeffs, tf, title):
    ts = np.linspace(0, tf, 200)
    pos, vel, acc = zip(*[poly_eval(coeffs, t) for t in ts])
    fig, axes = plt.subplots(1, 3, figsize=(12, 3.5))
    for ax, data, label in zip(axes, [pos, vel, acc], ["Position", "Velocity", "Acceleration"]):
        ax.plot(ts, data)
        ax.set_title(label)
        ax.set_xlabel("t")
        ax.grid(True, linestyle="--", alpha=0.4)
    fig.suptitle(title)
    fig.tight_layout()
    return fig


with tab1:
    st.markdown("4 boundary conditions: start and end position, zero velocity at both ends.")
    col1, col2, col3 = st.columns(3)
    theta_i = col1.number_input("theta_i (deg)", value=20.0, key="c_ti")
    theta_f = col2.number_input("theta_f (deg)", value=80.0, key="c_tf")
    tf = col3.number_input("t_f (seconds)", min_value=0.01, value=4.0, key="c_tfval")

    coeffs = cubic_coeffs(theta_i, theta_f, tf)
    st.markdown(
        f"theta(t) = {coeffs[0]:.4f} + {coeffs[1]:.4f}t + {coeffs[2]:.4f}t^2 + {coeffs[3]:.4f}t^3"
    )
    st.pyplot(plot_trajectory(coeffs, tf, "Cubic trajectory"))

with tab2:
    st.markdown("6 boundary conditions: start/end position, velocity, and acceleration.")
    col1, col2, col3 = st.columns(3)
    qi = col1.number_input("theta_i (deg)", value=0.0, key="q_ti")
    qi_dot = col2.number_input("theta_i' (deg/s)", value=0.0, key="q_tid")
    qi_ddot = col3.number_input("theta_i'' (deg/s^2)", value=0.0, key="q_tidd")
    col4, col5, col6 = st.columns(3)
    qf = col4.number_input("theta_f (deg)", value=90.0, key="q_tf")
    qf_dot = col5.number_input("theta_f' (deg/s)", value=0.0, key="q_tfd")
    qf_ddot = col6.number_input("theta_f'' (deg/s^2)", value=0.0, key="q_tfdd")
    tfq = st.number_input("t_f (seconds)", min_value=0.01, value=5.0, key="q_tfval")

    qcoeffs = quintic_coeffs(qi, qi_dot, qi_ddot, qf, qf_dot, qf_ddot, tfq)
    st.markdown("Coefficients (C0..C5): " + ", ".join(f"{c:.4f}" for c in qcoeffs))
    st.pyplot(plot_trajectory(qcoeffs, tfq, "Quintic trajectory"))

with tab3:
    st.markdown("Constant-velocity middle section with a parabolic blend at each end.")
    col1, col2, col3 = st.columns(3)
    p_ti = col1.number_input("theta_i (deg)", value=20.0, key="p_ti")
    p_tf = col2.number_input("theta_f (deg)", value=74.0, key="p_tf")
    p_tfval = col3.number_input("t_f (seconds)", min_value=0.01, value=12.0, key="p_tfval")
    col4, col5 = st.columns(2)
    p_accel = col4.number_input("acceleration (deg/s^2)", min_value=0.01, value=2.0, key="p_accel")
    p_tb = col5.number_input("blend duration t_b (seconds)", min_value=0.01, value=3.0, key="p_tb")

    result = parabolic_blend(p_ti, p_tf, p_tfval, p_accel, p_tb)
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("theta_A", f"{result['theta_a']:.2f} deg")
    c2.metric("theta'_A", f"{result['vel_a']:.2f} deg/s")
    c3.metric("theta_B", f"{result['theta_b']:.2f} deg")
    c4.metric("Linear velocity", f"{result['linear_velocity']:.2f} deg/s")
    st.caption(
        "For a physically consistent blend, theta'_A should equal the linear velocity."
    )
