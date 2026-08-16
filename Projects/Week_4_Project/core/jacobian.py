"""Jacobian and singularity analysis of a 2-DoF planar arm, from Lecture 6.

Forward kinematics:
    Px = L1*cos(theta1) + L2*cos(theta1+theta2)
    Py = L1*sin(theta1) + L2*sin(theta1+theta2)

The Jacobian relates joint velocities to Cartesian velocities: V = J(theta) * theta'.
A pose is singular when det(J) = 0, since J is then not invertible and the
robot loses a degree of freedom.
"""

import numpy as np


def jacobian(l1: float, l2: float, theta1: float, theta2: float) -> np.ndarray:
    j11 = -l1 * np.sin(theta1) - l2 * np.sin(theta1 + theta2)
    j12 = -l2 * np.sin(theta1 + theta2)
    j21 = l1 * np.cos(theta1) + l2 * np.cos(theta1 + theta2)
    j22 = l2 * np.cos(theta1 + theta2)
    return np.array([[j11, j12], [j21, j22]])


def determinant(l1: float, l2: float, theta1: float, theta2: float) -> float:
    """Closed form from the notes: det(J) = L1 * L2 * sin(theta2)."""
    j = jacobian(l1, l2, theta1, theta2)
    return float(np.linalg.det(j))


def is_singular(theta2: float, tol: float = 1e-6) -> bool:
    return abs(np.sin(theta2)) < tol
