"""Trajectory planning in joint space, from Lectures 4-5.

Three techniques are covered:
  - Cubic polynomial: 4 boundary conditions (start/end position, zero
    start/end velocity).
  - Quintic (5th-order) polynomial: 6 boundary conditions (start/end
    position, velocity, and acceleration).
  - Linear trajectory with parabolic blends: constant-velocity middle
    section with a parabolic ramp-up/ramp-down at each end, avoiding the
    infinite acceleration a pure linear trajectory would require.
"""

import numpy as np


def cubic_coeffs(theta_i: float, theta_f: float, tf: float):
    """Solves the 4-condition cubic: theta(0)=theta_i, theta'(0)=0,
    theta(tf)=theta_f, theta'(tf)=0.
    """
    delta = theta_f - theta_i
    c0 = theta_i
    c1 = 0.0
    c2 = 3 * delta / tf ** 2
    c3 = -2 * delta / tf ** 3
    return [c0, c1, c2, c3]


def quintic_coeffs(theta_i, theta_i_dot, theta_i_ddot, theta_f, theta_f_dot, theta_f_ddot, tf):
    """Solves the 6-condition quintic for position, velocity, and
    acceleration at both ends, via a direct linear solve rather than a
    memorized closed form.
    """
    c0 = theta_i
    c1 = theta_i_dot
    c2 = theta_i_ddot / 2

    a = np.array([
        [tf ** 3, tf ** 4, tf ** 5],
        [3 * tf ** 2, 4 * tf ** 3, 5 * tf ** 4],
        [6 * tf, 12 * tf ** 2, 20 * tf ** 3],
    ])
    b = np.array([
        theta_f - c0 - c1 * tf - c2 * tf ** 2,
        theta_f_dot - c1 - 2 * c2 * tf,
        theta_f_ddot - 2 * c2,
    ])
    c3, c4, c5 = np.linalg.solve(a, b)
    return [c0, c1, c2, c3, c4, c5]


def poly_eval(coeffs: list, t: float):
    """Returns (position, velocity, acceleration) of a polynomial with the
    given coefficients (coeffs[i] is the coefficient of t^i) at time t.
    """
    position = sum(c * t ** i for i, c in enumerate(coeffs))
    velocity = sum(i * c * t ** (i - 1) for i, c in enumerate(coeffs) if i >= 1)
    acceleration = sum(i * (i - 1) * c * t ** (i - 2) for i, c in enumerate(coeffs) if i >= 2)
    return position, velocity, acceleration


def parabolic_blend(theta_i: float, theta_f: float, tf: float, accel: float, tb: float):
    """Linear trajectory with symmetric parabolic blends of duration tb at
    each end. Returns the displacement and velocity at the end of the
    start blend (Junction A) and the start of the end blend (Junction B),
    plus the constant linear velocity in between.
    """
    theta_a = theta_i + 0.5 * accel * tb ** 2
    vel_a = accel * tb
    theta_b = theta_f - (theta_a - theta_i)
    linear_velocity = (theta_b - theta_a) / (tf - 2 * tb)
    return {
        "theta_a": theta_a,
        "vel_a": vel_a,
        "theta_b": theta_b,
        "linear_velocity": linear_velocity,
    }
