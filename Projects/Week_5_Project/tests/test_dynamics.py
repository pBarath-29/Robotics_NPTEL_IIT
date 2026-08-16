import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import numpy as np
import pytest
from core.dynamics import (
    compute_torques,
    gravity_only_torques,
    potential_energy,
    DYNAMIC_COUPLING_SYMMETRY_HOLDS,
)


def test_dynamic_coupling_symmetry_holds():
    # Lecture 4 states D_12 always equals D_21 -- verified symbolically
    # once at module import.
    assert DYNAMIC_COUPLING_SYMMETRY_HOLDS is True


def test_gravity_only_torque_matches_potential_energy_gradient():
    m1, m2, l1, l2, i1, i2, g = 2.0, 1.5, 1.0, 0.8, 0.05, 0.03, 9.81
    theta1, theta2 = np.deg2rad(30), np.deg2rad(45)

    tau1, tau2 = gravity_only_torques(theta1, theta2, m1, m2, l1, l2, i1, i2, g)

    eps = 1e-6
    p0 = potential_energy(theta1, theta2, m1, m2, l1, l2, g)
    p1 = potential_energy(theta1 + eps, theta2, m1, m2, l1, l2, g)
    p2 = potential_energy(theta1, theta2 + eps, m1, m2, l1, l2, g)
    numeric_dp_dtheta1 = (p1 - p0) / eps
    numeric_dp_dtheta2 = (p2 - p0) / eps

    assert tau1 == pytest.approx(numeric_dp_dtheta1, abs=1e-4)
    assert tau2 == pytest.approx(numeric_dp_dtheta2, abs=1e-4)


def test_zero_gravity_zero_motion_gives_zero_torque():
    m1, m2, l1, l2, i1, i2 = 2.0, 1.5, 1.0, 0.8, 0.05, 0.03
    theta1, theta2 = np.deg2rad(20), np.deg2rad(-10)
    tau1, tau2 = compute_torques(theta1, theta2, 0, 0, 0, 0, m1, m2, l1, l2, i1, i2, g=0.0)
    assert tau1 == pytest.approx(0.0, abs=1e-9)
    assert tau2 == pytest.approx(0.0, abs=1e-9)


def test_torque_changes_with_acceleration_only():
    m1, m2, l1, l2, i1, i2 = 2.0, 1.5, 1.0, 0.8, 0.05, 0.03
    theta1, theta2 = np.deg2rad(0), np.deg2rad(0)
    tau_still = compute_torques(theta1, theta2, 0, 0, 0, 0, m1, m2, l1, l2, i1, i2, g=0.0)
    tau_accel = compute_torques(theta1, theta2, 0, 0, 1.0, 0, m1, m2, l1, l2, i1, i2, g=0.0)
    assert tau_still != tau_accel
