"""Triangulation range sensor, from Lecture 4.

The emitter and receiver are separated by a fixed baseline 'a'. When the
beam, fired at angle theta, reflects perpendicular into the receiver, a
right triangle is formed, giving distance d = a * tan(theta).
"""

import numpy as np


def triangulation_distance(baseline: float, theta_rad: float) -> float:
    return baseline * np.tan(theta_rad)


def triangulation_angle(baseline: float, distance: float) -> float:
    return np.arctan2(distance, baseline)
