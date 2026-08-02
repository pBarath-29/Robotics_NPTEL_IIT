import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import numpy as np
import pytest
from core.dh import (
    forward_kinematics,
    two_dof_planar_dh_table,
    two_dof_planar_expected_position,
    minimover_dh_table,
)


def test_2dof_planar_matches_closed_form():
    l1, l2 = 3.0, 2.0
    theta1, theta2 = np.deg2rad(30), np.deg2rad(45)
    dh_table = two_dof_planar_dh_table(l1, l2, theta1, theta2)
    t_final, _ = forward_kinematics(dh_table)
    position = t_final[:3, 3]
    expected = two_dof_planar_expected_position(l1, l2, theta1, theta2)
    assert position == pytest.approx(expected, abs=1e-9)


def test_2dof_planar_zero_angles_fully_extended():
    l1, l2 = 3.0, 2.0
    dh_table = two_dof_planar_dh_table(l1, l2, 0.0, 0.0)
    t_final, _ = forward_kinematics(dh_table)
    position = t_final[:3, 3]
    assert position == pytest.approx([l1 + l2, 0.0, 0.0], abs=1e-9)


def test_minimover_table_builds_and_runs():
    thetas = [np.deg2rad(t) for t in [10, 20, 30, 40, 50]]
    dh_table = minimover_dh_table(2.0, 1.5, thetas)
    assert len(dh_table) == 5
    t_final, frames = forward_kinematics(dh_table)
    assert len(frames) == 6
    assert np.all(np.isfinite(t_final))
    # bottom row of any valid homogeneous transform must be [0,0,0,1]
    assert t_final[3, :] == pytest.approx([0, 0, 0, 1])
