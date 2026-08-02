import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import numpy as np
import pytest
from core.coordinates import cylindrical_to_cartesian, spherical_to_cartesian


def test_cylindrical_matches_notes_formula():
    r, theta, z = 5.0, np.deg2rad(30), 2.0
    qx, qy, qz = cylindrical_to_cartesian(r, theta, z)
    assert qx == pytest.approx(r * np.cos(theta))
    assert qy == pytest.approx(r * np.sin(theta))
    assert qz == pytest.approx(z)


def test_spherical_matches_notes_formula():
    r, alpha, beta = 5.0, np.deg2rad(60), np.deg2rad(40)
    qx, qy, qz = spherical_to_cartesian(r, alpha, beta)
    assert qx == pytest.approx(r * np.sin(alpha) * np.cos(beta))
    assert qy == pytest.approx(r * np.sin(alpha) * np.sin(beta))
    assert qz == pytest.approx(r * np.cos(alpha))


def test_spherical_radius_is_preserved():
    qx, qy, qz = spherical_to_cartesian(7.0, np.deg2rad(50), np.deg2rad(80))
    assert np.sqrt(qx ** 2 + qy ** 2 + qz ** 2) == pytest.approx(7.0)
