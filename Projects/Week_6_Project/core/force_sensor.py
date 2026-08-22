"""Wrist force/moment sensor, from Lecture 3.

A cantilever deflection bar obeys, within its elastic limit:
    delta = (P * L^3) / (3 * E * I)
Eight strain-gauge readings (one pair per bar, four bars) are combined
into the six force/moment components (Fx, Fy, Fz, Mx, My, Mz) via a 6x8
calibration matrix: [F] = C_M * [W], where [W] is the 8x1 raw reading
vector.
"""

import numpy as np


def cantilever_deflection(p: float, l: float, e: float, i: float) -> float:
    return (p * l ** 3) / (3 * e * i)


def cantilever_load(delta: float, l: float, e: float, i: float) -> float:
    return (delta * 3 * e * i) / (l ** 3)


def apply_calibration_matrix(raw_readings: np.ndarray, calibration_matrix: np.ndarray) -> np.ndarray:
    """raw_readings: 8-element vector (W1..W8).
    calibration_matrix: 6x8 matrix (C_M).
    Returns the 6-element [Fx, Fy, Fz, Mx, My, Mz] vector.
    """
    raw_readings = np.asarray(raw_readings).reshape(8, 1)
    result = calibration_matrix @ raw_readings
    return result.flatten()
