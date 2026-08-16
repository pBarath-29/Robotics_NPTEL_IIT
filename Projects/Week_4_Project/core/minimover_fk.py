"""Forward kinematics of the MINIMOVER 5-DoF manipulator, from Lecture 1.

DH table (matching the joint configuration T-R-R-R-T, and the dummy 6th
frame copied onto the end-effector):
    Frame 1 (Twisting): theta1, d=0, alpha=-90deg, a=0
    Frame 2 (Revolute): theta2, d=0, alpha=0,      a=L1
    Frame 3 (Revolute): theta3, d=0, alpha=0,      a=L2
    Frame 4 (Revolute): theta4, d=0, alpha=90deg,  a=0
    Frame 5 (Twisting): theta5, d=0, alpha=0,      a=0

The notes give a closed-form position result directly:
    px = cos(theta1) * [L1*cos(theta2) + L2*cos(theta2 + theta3)]
    py = sin(theta1) * [L1*cos(theta2) + L2*cos(theta2 + theta3)]
    pz = -L1*sin(theta2) - L2*sin(theta2 + theta3)
which only depends on theta1, theta2, theta3 -- theta4 and theta5 only
affect the end-effector's orientation, not its position, since the last
two frames add no further translation (a4 = a5 = 0).
"""

import numpy as np
from core.dh import forward_kinematics


def minimover_dh_table(l1: float, l2: float, thetas: list) -> list:
    """thetas: [theta1..theta5] in radians."""
    alphas = [np.deg2rad(-90), 0, 0, np.deg2rad(90), 0]
    a_values = [0, l1, l2, 0, 0]
    return [
        {"theta": thetas[i], "d": 0, "alpha": alphas[i], "a": a_values[i]}
        for i in range(5)
    ]


def closed_form_position(l1: float, l2: float, theta1: float, theta2: float, theta3: float):
    px = np.cos(theta1) * (l1 * np.cos(theta2) + l2 * np.cos(theta2 + theta3))
    py = np.sin(theta1) * (l1 * np.cos(theta2) + l2 * np.cos(theta2 + theta3))
    pz = -l1 * np.sin(theta2) - l2 * np.sin(theta2 + theta3)
    return px, py, pz


def compute(l1: float, l2: float, thetas: list):
    """Full forward kinematics via the DH chain. Returns (T_final, frames)."""
    dh_table = minimover_dh_table(l1, l2, thetas)
    return forward_kinematics(dh_table)
