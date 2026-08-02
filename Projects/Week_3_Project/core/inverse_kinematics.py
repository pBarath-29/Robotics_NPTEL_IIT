"""Inverse kinematics for the 2-DoF planar manipulator, from Lecture 5.

Given a target end-effector position (qx, qy) and the two link lengths,
find the joint angles (theta1, theta2) that reach it. There are generally
two solutions (an "elbow up"/right-hand and an "elbow down"/left-hand
configuration), matching the notes' point that inverse kinematics rarely
has a single solution.

theta2 is found first via the law of cosines (the notes' cos(theta2)
formula), then theta1 is found by substitution. This implementation uses
atan2 for the theta1 substitution step, a numerically robust equivalent of
the notes' tan^-1-based approach that also handles all quadrants correctly.
"""

import numpy as np


class UnreachableTarget(Exception):
    pass


def solve_2dof(l1: float, l2: float, qx: float, qy: float):
    """Returns a list of up to two (theta1, theta2, label) solutions, in
    radians, for the right-hand and left-hand elbow configurations.
    """
    d_sq = qx ** 2 + qy ** 2
    cos_theta2 = (d_sq - l1 ** 2 - l2 ** 2) / (2 * l1 * l2)

    if cos_theta2 < -1 - 1e-9 or cos_theta2 > 1 + 1e-9:
        raise UnreachableTarget(
            f"Target ({qx}, {qy}) is out of reach for link lengths L1={l1}, L2={l2}."
        )
    cos_theta2 = np.clip(cos_theta2, -1.0, 1.0)

    solutions = []
    for sign, label in [(1, "Right-hand (elbow up)"), (-1, "Left-hand (elbow down)")]:
        theta2 = sign * np.arccos(cos_theta2)
        k1 = l1 + l2 * np.cos(theta2)
        k2 = l2 * np.sin(theta2)
        theta1 = np.arctan2(qy, qx) - np.arctan2(k2, k1)
        solutions.append((theta1, theta2, label))
    return solutions
