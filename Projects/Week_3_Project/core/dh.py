"""Denavit-Hartenberg notation and forward kinematics, from Lectures 3-4-5.

The four DH parameters per joint:
  a_i     Link Length: mutual perpendicular distance between Axis_{i-1} and Axis_i.
  alpha_i Angle of Twist: angle between Axis_{i-1} and Axis_i about the common normal.
  d_i     Link Offset: distance along Axis_{i-1} (the variable for a prismatic joint).
  theta_i Joint Angle: angle about Axis_{i-1} (the variable for a revolute joint).

The transformation from frame i-1 to frame i is built from two "screw"
motions (a rotation about an axis followed by a translation along that
same axis):
    Screw Z: Rot(Z, theta_i) then Trans(Z, d_i)
    Screw X: Rot(X, alpha_i) then Trans(X, a_i)
    T_i^(i-1) = Screw_Z * Screw_X
              = Rot(Z, theta_i) * Trans(Z, d_i) * Rot(X, alpha_i) * Trans(X, a_i)
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
    """4x4 transform from frame i-1 to frame i, given the DH parameters
    (theta and alpha in radians).
    """
    return _rot_z4(theta) @ _trans4(0, 0, d) @ _rot_x4(alpha) @ _trans4(a, 0, 0)


def forward_kinematics(dh_table: list):
    """dh_table: list of dicts with keys theta, d, alpha, a (radians for
    theta/alpha). Returns (T_final, list_of_intermediate_frames).
    """
    t = np.eye(4)
    frames = [t.copy()]
    for row in dh_table:
        ti = dh_transform(row["theta"], row["d"], row["alpha"], row["a"])
        t = t @ ti
        frames.append(t.copy())
    return t, frames


def end_effector_position(dh_table: list):
    t, _ = forward_kinematics(dh_table)
    return t[:3, 3]


# 2-DoF planar serial manipulator case study (Lecture 4).
def two_dof_planar_dh_table(l1: float, l2: float, theta1: float, theta2: float) -> list:
    return [
        {"theta": theta1, "d": 0, "alpha": 0, "a": l1},
        {"theta": theta2, "d": 0, "alpha": 0, "a": l2},
    ]


def two_dof_planar_expected_position(l1: float, l2: float, theta1: float, theta2: float):
    """Closed-form position given directly in the notes, used to verify
    the general DH forward-kinematics engine above.
    """
    qx = l1 * np.cos(theta1) + l2 * np.cos(theta1 + theta2)
    qy = l1 * np.sin(theta1) + l2 * np.sin(theta1 + theta2)
    return qx, qy, 0.0


# MINIMOVER 5-DoF spatial serial manipulator case study (Lecture 5),
# joint configuration T-R-R-R-T.
def minimover_dh_table(l1: float, l2: float, thetas: list) -> list:
    """thetas: [theta1..theta5] in radians."""
    alphas = [np.deg2rad(-90), 0, 0, np.deg2rad(90), 0]
    a_values = [0, l1, l2, 0, 0]
    return [
        {"theta": thetas[i], "d": 0, "alpha": alphas[i], "a": a_values[i]}
        for i in range(5)
    ]
