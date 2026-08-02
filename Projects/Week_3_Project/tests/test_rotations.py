import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import numpy as np
import pytest
from core.rotations import rot_x, rot_y, rot_z, compose_rotations, check_rotation_properties


@pytest.mark.parametrize("rot_fn", [rot_x, rot_y, rot_z])
def test_elementary_rotations_are_valid(rot_fn):
    r = rot_fn(np.deg2rad(37))
    result = check_rotation_properties(r)
    assert result["is_valid_rotation"]


def test_composite_rotation_matches_notes_example():
    # Notes example: rotate Z by alpha, then Y by beta, then X by gamma
    # -> ROT_comp = Rot(X, gamma) * Rot(Y, beta) * Rot(Z, alpha)
    alpha, beta, gamma = np.deg2rad(10), np.deg2rad(20), np.deg2rad(30)
    composite = compose_rotations([("Z", alpha), ("Y", beta), ("X", gamma)])
    expected = rot_x(gamma) @ rot_y(beta) @ rot_z(alpha)
    assert composite == pytest.approx(expected)


def test_rotation_is_non_commutative():
    a = compose_rotations([("X", np.deg2rad(30)), ("Y", np.deg2rad(45))])
    b = compose_rotations([("Y", np.deg2rad(45)), ("X", np.deg2rad(30))])
    assert not np.allclose(a, b)


def test_non_rotation_matrix_is_rejected():
    not_a_rotation = np.array([[2, 0, 0], [0, 1, 0], [0, 0, 1]])
    result = check_rotation_properties(not_a_rotation)
    assert not result["is_valid_rotation"]
