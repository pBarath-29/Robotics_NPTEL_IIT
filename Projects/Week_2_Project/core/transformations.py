"""Frame transformations, from Lecture 6 (frames, position, orientation) and
Lecture 7 (the explicit rotation matrix formulas, the translation operator,
and why matrix inversion in code avoids a naive determinant division).

Each operator returns a 4x4 homogeneous transformation matrix: a 3x3
rotation block in the top-left, a 3x1 translation vector in the top-right,
and the bottom row fixed at [0, 0, 0, 1], exactly as described in Lecture 7.
"""

import numpy as np


def rot_x(theta_rad: float) -> np.ndarray:
    c, s = np.cos(theta_rad), np.sin(theta_rad)
    return np.array([
        [1, 0, 0, 0],
        [0, c, -s, 0],
        [0, s, c, 0],
        [0, 0, 0, 1],
    ])


def rot_y(theta_rad: float) -> np.ndarray:
    c, s = np.cos(theta_rad), np.sin(theta_rad)
    return np.array([
        [c, 0, s, 0],
        [0, 1, 0, 0],
        [-s, 0, c, 0],
        [0, 0, 0, 1],
    ])


def rot_z(theta_rad: float) -> np.ndarray:
    c, s = np.cos(theta_rad), np.sin(theta_rad)
    return np.array([
        [c, -s, 0, 0],
        [s, c, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1],
    ])


def trans(a: float, b: float, c: float) -> np.ndarray:
    """Translation operator. Top-left 3x3 is the identity (no rotation),
    since a pure translation leaves the axes parallel to the universal frame.
    """
    return np.array([
        [1, 0, 0, a],
        [0, 1, 0, b],
        [0, 0, 1, c],
        [0, 0, 0, 1],
    ])


OPERATORS = {
    "Translate": trans,
    "Rotate X": rot_x,
    "Rotate Y": rot_y,
    "Rotate Z": rot_z,
}


def compose(matrices: list) -> np.ndarray:
    """Compose a sequence of 4x4 operators in order: T = T1 @ T2 @ ... @ Tn."""
    result = np.eye(4)
    for m in matrices:
        result = result @ m
    return result


def apply_to_point(transform: np.ndarray, point_xyz) -> np.ndarray:
    """Apply a 4x4 homogeneous transform to a 3D point, returning the
    transformed x, y, z (the homogeneous 1 is dropped from the output).
    """
    x, y, z = point_xyz
    q_b = np.array([x, y, z, 1.0])
    q_u = transform @ q_b
    return q_u[:3]


def invert(transform: np.ndarray) -> np.ndarray:
    """Invert a 4x4 homogeneous transform.

    The notes point out that inverting via Adjoint(T)/Determinant(T) is
    numerically fragile (a zero determinant causes a divide-by-zero/NaN),
    and that real implementations use row/column reduction instead.
    numpy.linalg.inv uses LU decomposition internally, which is exactly
    that kind of reduction-based approach rather than a naive adjoint
    division, so it is used here.
    """
    return np.linalg.inv(transform)
