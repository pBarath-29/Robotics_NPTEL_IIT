"""Boundary descriptors and object identification, from Lecture 2.

Chain codes trace a closed boundary as a sequence of fixed-length unit
steps in numbered directions (4-directional, 90 degrees apart, or
8-directional, 45 degrees apart).

Signatures plot the distance r from an object's center of mass to its
boundary as a function of angle theta: a constant line for a circle, and
a repeating peak-and-valley curve for a square (r = A at theta = 0,
r = A*sqrt(2) at theta = 45 degrees).

Compactness = Perimeter^2 / Area is used to identify a shape by comparing
against known reference values.
"""

import numpy as np

DIRECTIONS_4 = [(1, 0), (0, 1), (-1, 0), (0, -1)]
DIRECTIONS_8 = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]


def encode_chain(points: list, directions: list) -> list:
    """points: a closed boundary as a list of (x, y) integer grid points
    (the last point implicitly connects back to the first). Each
    consecutive step must be axis-aligned or (for 8-direction) diagonal,
    and may span more than one grid unit -- longer segments repeat their
    direction code once per unit step.
    """
    codes = []
    n = len(points)
    for i in range(n):
        x0, y0 = points[i]
        x1, y1 = points[(i + 1) % n]
        dx, dy = x1 - x0, y1 - y0
        length = max(abs(dx), abs(dy))
        if length == 0:
            continue
        step = (dx // length, dy // length)
        code = directions.index(step)
        codes.extend([code] * length)
    return codes


def circle_signature(theta_rad: np.ndarray, radius: float) -> np.ndarray:
    return np.full_like(theta_rad, radius)


def square_signature(theta_rad: np.ndarray, half_side: float) -> np.ndarray:
    theta_deg = np.rad2deg(theta_rad)
    folded_deg = np.mod(theta_deg + 45, 90) - 45
    return half_side / np.cos(np.deg2rad(folded_deg))


def compactness(perimeter: float, area: float) -> float:
    return perimeter ** 2 / area


REFERENCE_COMPACTNESS = {
    "Circle": 4 * np.pi,
    "Square": 16.0,
    "Equilateral Triangle": 12 * np.sqrt(3),
}


def closest_shape_match(measured_compactness: float) -> str:
    return min(REFERENCE_COMPACTNESS, key=lambda name: abs(REFERENCE_COMPACTNESS[name] - measured_compactness))
