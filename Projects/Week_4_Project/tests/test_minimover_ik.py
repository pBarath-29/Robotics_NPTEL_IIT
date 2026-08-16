import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import numpy as np
import pytest
from core.minimover_fk import compute
from core.minimover_ik import solve_full, solve_position, UnreachableTarget


def test_ik_round_trips_through_fk():
    l1, l2 = 2.0, 1.5
    true_thetas_deg = [25, 35, -20, 15, 55]
    true_thetas = [np.deg2rad(t) for t in true_thetas_deg]
    t_final, _ = compute(l1, l2, true_thetas)
    qx, qy, qz = t_final[:3, 3]
    r = t_final[:3, :3]

    solutions = solve_full(l1, l2, qx, qy, qz, r)
    assert len(solutions) == 2

    # At least one of the returned solutions must reproduce the true angles.
    def matches(sol):
        return np.allclose(sol[:5], true_thetas, atol=1e-6)

    assert any(matches(sol) for sol in solutions)


def test_ik_solutions_reach_the_target_position():
    l1, l2 = 2.0, 1.5
    true_thetas = [np.deg2rad(t) for t in [10, 40, -30, 5, 20]]
    t_final, _ = compute(l1, l2, true_thetas)
    qx, qy, qz = t_final[:3, 3]
    r = t_final[:3, :3]

    for theta1, theta2, theta3, theta4, theta5, _ in solve_full(l1, l2, qx, qy, qz, r):
        check, _ = compute(l1, l2, [theta1, theta2, theta3, theta4, theta5])
        assert check[:3, 3] == pytest.approx([qx, qy, qz], abs=1e-6)


def test_unreachable_target_raises():
    with pytest.raises(UnreachableTarget):
        solve_position(1.0, 1.0, 10.0, 10.0, 10.0)
