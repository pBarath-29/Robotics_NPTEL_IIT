"""Roll-Pitch-Yaw and Euler angle orientation, from Lecture 2.

RPY rotations are taken with respect to the fixed Universal frame, so the
composite rule applies directly:
    R_B_U(rpy) = Rot(Z, gamma) * Rot(Y, beta) * Rot(X, alpha)

Euler rotations are taken with respect to the moving Body frame. The notes'
approach: compute the rotation of the Universe with respect to the Body
using negative angles, then take the transpose (since inverse = transpose
for a pure rotation) to get the Body-with-respect-to-Universe matrix:
    R_U_B = Rot(X, -gamma) * Rot(Y, -beta) * Rot(Z, -alpha)
    R_B_U = transpose(R_U_B)

Angle extraction uses atan2 (a numerically robust form of the same
tan^-1 relationships given in the notes, handling quadrants correctly).
"""

import numpy as np
from core.rotations import rot_x, rot_y, rot_z


def rpy_to_matrix(alpha_rad: float, beta_rad: float, gamma_rad: float) -> np.ndarray:
    return rot_z(gamma_rad) @ rot_y(beta_rad) @ rot_x(alpha_rad)


def matrix_to_rpy(r: np.ndarray):
    alpha = np.arctan2(r[2, 1], r[2, 2])
    beta = np.arctan2(-r[2, 0], np.sqrt(r[0, 0] ** 2 + r[1, 0] ** 2))
    gamma = np.arctan2(r[1, 0], r[0, 0])
    return alpha, beta, gamma


def euler_to_matrix(alpha_rad: float, beta_rad: float, gamma_rad: float) -> np.ndarray:
    r_u_b = rot_x(-gamma_rad) @ rot_y(-beta_rad) @ rot_z(-alpha_rad)
    return r_u_b.T


def matrix_to_euler(r: np.ndarray):
    alpha = np.arctan2(r[1, 0], r[0, 0])
    beta = np.arctan2(-r[2, 0], np.sqrt(r[0, 0] ** 2 + r[1, 0] ** 2))
    gamma = np.arctan2(r[2, 1], r[2, 2])
    return alpha, beta, gamma
