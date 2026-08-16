"""Generic Denavit-Hartenberg transform and forward kinematics engine.

Same Screw Z then Screw X convention used throughout the course:
    T_i^(i-1) = Rot(Z, theta_i) * Trans(Z, d_i) * Rot(X, alpha_i) * Trans(X, a_i)
"""

import numpy as np


def _rot_z4(theta):
    c, s = np.cos(theta), np.sin(theta)
    return np.array([[c, -s, 0, 0], [s, c, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])


def _rot_x4(theta):
    c, s = np.cos(theta), np.sin(theta)
    return np.array([[1, 0, 0, 0], [0, c, -s, 0], [0, s, c, 0], [0, 0, 0, 1]])


def _trans4(x, y, z):
    return np.array([[1, 0, 0, x], [0, 1, 0, y], [0, 0, 1, z], [0, 0, 0, 1]])


def dh_transform(theta: float, d: float, alpha: float, a: float) -> np.ndarray:
    return _rot_z4(theta) @ _trans4(0, 0, d) @ _rot_x4(alpha) @ _trans4(a, 0, 0)


def forward_kinematics(dh_table: list):
    """dh_table: list of dicts with keys theta, d, alpha, a (radians).
    Returns (T_final, list_of_intermediate_frames).
    """
    t = np.eye(4)
    frames = [t.copy()]
    for row in dh_table:
        ti = dh_transform(row["theta"], row["d"], row["alpha"], row["a"])
        t = t @ ti
        frames.append(t.copy())
    return t, frames
