"""Rotation matrix properties and the composite rotation rule, from
Lecture 1: "Rotation Matrices & Coordinate System Transformations".

Properties of a valid 3x3 rotation matrix (all checked here):
  - Each row and each column is a unit vector.
  - Any two different rows (or columns) are orthogonal (dot product 0).
  - The inverse equals the transpose (true only for pure rotation, not for
    a full transformation matrix that also has translation).

Composite rotation rule: transformations are multiplied right-to-left --
the first rotation stated in a sequence ends up at the far right of the
product, and each subsequent one is multiplied to the left.
"""

import numpy as np

AXES = {"X", "Y", "Z"}


def rot_x(theta_rad: float) -> np.ndarray:
    c, s = np.cos(theta_rad), np.sin(theta_rad)
    return np.array([
        [1, 0, 0],
        [0, c, -s],
        [0, s, c],
    ])


def rot_y(theta_rad: float) -> np.ndarray:
    c, s = np.cos(theta_rad), np.sin(theta_rad)
    return np.array([
        [c, 0, s],
        [0, 1, 0],
        [-s, 0, c],
    ])


def rot_z(theta_rad: float) -> np.ndarray:
    c, s = np.cos(theta_rad), np.sin(theta_rad)
    return np.array([
        [c, -s, 0],
        [s, c, 0],
        [0, 0, 1],
    ])


ROTATORS = {"X": rot_x, "Y": rot_y, "Z": rot_z}


def compose_rotations(sequence: list) -> np.ndarray:
    """Compose a sequence of (axis, angle_rad) rotations using the
    composite rule: the first rotation performed ends up at the far right
    of the matrix product, so each new rotation is left-multiplied onto
    the running result as we iterate through the stated order.
    """
    result = np.eye(3)
    for axis, angle in sequence:
        result = ROTATORS[axis](angle) @ result
    return result


def row_and_column_norms(matrix: np.ndarray):
    row_norms = [np.linalg.norm(matrix[i, :]) for i in range(3)]
    col_norms = [np.linalg.norm(matrix[:, i]) for i in range(3)]
    return row_norms, col_norms


def is_orthogonal_matrix(matrix: np.ndarray, tol: float = 1e-9) -> bool:
    """Every distinct pair of rows (and of columns) must have a zero dot product."""
    for i in range(3):
        for j in range(i + 1, 3):
            if abs(np.dot(matrix[i, :], matrix[j, :])) > tol:
                return False
            if abs(np.dot(matrix[:, i], matrix[:, j])) > tol:
                return False
    return True


def inverse_equals_transpose(matrix: np.ndarray, tol: float = 1e-9) -> bool:
    return np.allclose(np.linalg.inv(matrix), matrix.T, atol=tol)


def check_rotation_properties(matrix: np.ndarray, tol: float = 1e-6) -> dict:
    row_norms, col_norms = row_and_column_norms(matrix)
    unit_vectors = all(abs(n - 1.0) < tol for n in row_norms + col_norms)
    orthogonal = is_orthogonal_matrix(matrix, tol)
    inv_eq_transpose = inverse_equals_transpose(matrix, tol)
    return {
        "row_norms": row_norms,
        "col_norms": col_norms,
        "unit_vectors": unit_vectors,
        "orthogonal": orthogonal,
        "inverse_equals_transpose": inv_eq_transpose,
        "is_valid_rotation": unit_vectors and orthogonal and inv_eq_transpose,
    }
