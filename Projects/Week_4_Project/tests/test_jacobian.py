import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import numpy as np
import pytest
from core.jacobian import jacobian, determinant, is_singular


def test_determinant_matches_closed_form():
    l1, l2 = 3.0, 2.0
    theta1, theta2 = np.deg2rad(40), np.deg2rad(65)
    det = determinant(l1, l2, theta1, theta2)
    expected = l1 * l2 * np.sin(theta2)
    assert det == pytest.approx(expected)


def test_fully_stretched_is_singular():
    assert is_singular(0.0)


def test_folded_back_is_singular():
    assert is_singular(np.pi)


def test_generic_pose_is_not_singular():
    assert not is_singular(np.deg2rad(65))


def test_jacobian_shape():
    j = jacobian(3.0, 2.0, 0.5, 0.5)
    assert j.shape == (2, 2)
