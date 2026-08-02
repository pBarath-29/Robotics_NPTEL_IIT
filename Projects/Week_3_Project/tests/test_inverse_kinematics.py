import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import numpy as np
import pytest
from core.inverse_kinematics import solve_2dof, UnreachableTarget
from core.dh import two_dof_planar_dh_table, forward_kinematics


def _reaches(l1, l2, theta1, theta2, target, tol=1e-6):
    dh_table = two_dof_planar_dh_table(l1, l2, theta1, theta2)
    t_final, _ = forward_kinematics(dh_table)
    pos = t_final[:2, 3]
    return np.allclose(pos, target, atol=tol)


def test_inverse_kinematics_round_trips_through_forward_kinematics():
    l1, l2 = 3.0, 2.0
    theta1_true, theta2_true = np.deg2rad(30), np.deg2rad(45)
    dh_table = two_dof_planar_dh_table(l1, l2, theta1_true, theta2_true)
    t_final, _ = forward_kinematics(dh_table)
    qx, qy = t_final[0, 3], t_final[1, 3]

    solutions = solve_2dof(l1, l2, qx, qy)
    assert len(solutions) == 2
    # At least one of the two IK solutions must reproduce the target point.
    assert any(_reaches(l1, l2, t1, t2, (qx, qy)) for t1, t2, _ in solutions)


def test_two_solutions_both_reach_target_when_distinct():
    l1, l2 = 3.0, 2.0
    qx, qy = 4.0, 2.0
    solutions = solve_2dof(l1, l2, qx, qy)
    for theta1, theta2, _ in solutions:
        assert _reaches(l1, l2, theta1, theta2, (qx, qy))


def test_unreachable_target_raises():
    with pytest.raises(UnreachableTarget):
        solve_2dof(1.0, 1.0, 10.0, 10.0)
