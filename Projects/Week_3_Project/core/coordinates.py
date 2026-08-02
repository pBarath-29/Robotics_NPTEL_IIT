"""Cylindrical and spherical coordinate mapping, from Lecture 1.

Both are derived by applying the composite rotation/translation rule to a
specific sequence of elementary moves, which multiply out to these closed
form conversions.
"""

import numpy as np


def cylindrical_to_cartesian(r: float, theta_rad: float, z: float):
    """Sequence: Translate X by r, Rotate Z by theta, Translate Z by z."""
    qx = r * np.cos(theta_rad)
    qy = r * np.sin(theta_rad)
    qz = z
    return qx, qy, qz


def spherical_to_cartesian(r: float, alpha_rad: float, beta_rad: float):
    """Sequence: Translate Z by r, Rotate Y by alpha, Rotate Z by beta."""
    qx = r * np.sin(alpha_rad) * np.cos(beta_rad)
    qy = r * np.sin(alpha_rad) * np.sin(beta_rad)
    qz = r * np.cos(alpha_rad)
    return qx, qy, qz
