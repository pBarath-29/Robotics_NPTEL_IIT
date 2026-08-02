import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import numpy as np
import pytest
from core.orientation import rpy_to_matrix, matrix_to_rpy, euler_to_matrix, matrix_to_euler
from core.rotations import check_rotation_properties


def test_rpy_round_trip():
    alpha, beta, gamma = np.deg2rad(20), np.deg2rad(30), np.deg2rad(40)
    r = rpy_to_matrix(alpha, beta, gamma)
    a2, b2, g2 = matrix_to_rpy(r)
    assert a2 == pytest.approx(alpha, abs=1e-9)
    assert b2 == pytest.approx(beta, abs=1e-9)
    assert g2 == pytest.approx(gamma, abs=1e-9)


def test_euler_round_trip():
    alpha, beta, gamma = np.deg2rad(15), np.deg2rad(-25), np.deg2rad(35)
    r = euler_to_matrix(alpha, beta, gamma)
    a2, b2, g2 = matrix_to_euler(r)
    assert a2 == pytest.approx(alpha, abs=1e-9)
    assert b2 == pytest.approx(beta, abs=1e-9)
    assert g2 == pytest.approx(gamma, abs=1e-9)


def test_rpy_matrix_is_a_valid_rotation():
    r = rpy_to_matrix(np.deg2rad(10), np.deg2rad(20), np.deg2rad(30))
    assert check_rotation_properties(r)["is_valid_rotation"]


def test_euler_matrix_is_a_valid_rotation():
    r = euler_to_matrix(np.deg2rad(10), np.deg2rad(20), np.deg2rad(30))
    assert check_rotation_properties(r)["is_valid_rotation"]
