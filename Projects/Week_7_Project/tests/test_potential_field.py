import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import numpy as np
import pytest
from core.potential_field import attractive_force, repulsive_force, plan_path


def test_attractive_force_zero_at_goal():
    f = attractive_force((3, 3), (3, 3), k_att=1.0)
    assert np.linalg.norm(f) == pytest.approx(0.0)


def test_attractive_force_proportional_to_distance():
    f_near = attractive_force((1, 0), (0, 0), k_att=2.0)
    f_far = attractive_force((5, 0), (0, 0), k_att=2.0)
    assert np.linalg.norm(f_far) == pytest.approx(5 * np.linalg.norm(f_near))


def test_repulsive_force_zero_outside_influence_radius():
    f = repulsive_force((10, 10), obstacle_center=(0, 0), obstacle_radius=1.0,
                         influence_radius=2.0, k_rep=1.0)
    assert np.linalg.norm(f) == pytest.approx(0.0)


def test_repulsive_force_grows_closer_to_obstacle():
    far = repulsive_force((3, 0), obstacle_center=(0, 0), obstacle_radius=1.0,
                           influence_radius=3.0, k_rep=1.0)
    near = repulsive_force((1.5, 0), obstacle_center=(0, 0), obstacle_radius=1.0,
                            influence_radius=3.0, k_rep=1.0)
    assert np.linalg.norm(near) > np.linalg.norm(far)


def test_clean_path_with_no_obstacles_reaches_goal():
    path, status = plan_path((0, 0), (5, 5), obstacles=[])
    assert status == "reached"
    assert np.linalg.norm(np.array(path[-1]) - np.array([5, 5])) < 0.2


def test_offset_single_obstacle_is_navigated_successfully():
    path, status = plan_path((0, 0), (10, 0), obstacles=[((5, 0.3), 1.0)],
                              k_rep=5.0, influence_radius=2.5)
    assert status == "reached"


def test_u_shaped_trap_produces_local_minimum():
    # Matches the notes' description of the Local Minima Problem: a
    # concave (U-shaped) arrangement of obstacles traps the robot before
    # it reaches the goal.
    start, goal = (0, 0), (0, 20)
    obstacles = [((0, 6), 1.5), ((-3, 3), 1.5), ((3, 3), 1.5)]
    path, status = plan_path(start, goal, obstacles, k_att=1.0, k_rep=8.0, influence_radius=3.0)
    assert status == "stuck"
    assert np.linalg.norm(np.array(path[-1]) - np.array(goal)) > 1.0
