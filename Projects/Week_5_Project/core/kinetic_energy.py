"""Trace notation for kinetic energy, from Lecture 2.

Squaring a 3D velocity vector [vx, vy, vz] as an outer product V*V^T
produces a 3x3 matrix whose diagonal sums to vx^2 + vy^2 + vz^2 -- the
Trace of that matrix. This is why the notes write the kinetic energy of a
differential mass as dK = (1/2) * Trace(V * V^T) * dm.
"""

import numpy as np


def velocity_outer_product(vx: float, vy: float, vz: float) -> np.ndarray:
    v = np.array([[vx], [vy], [vz]])
    return v @ v.T


def trace_kinetic_energy(vx: float, vy: float, vz: float, dm: float) -> float:
    outer = velocity_outer_product(vx, vy, vz)
    return 0.5 * np.trace(outer) * dm


def direct_kinetic_energy(vx: float, vy: float, vz: float, dm: float) -> float:
    """The familiar (1/2)*m*V^2 form, for comparison."""
    return 0.5 * dm * (vx ** 2 + vy ** 2 + vz ** 2)
