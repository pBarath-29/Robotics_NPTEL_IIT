import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import numpy as np
import pytest
from core.range_sensor import triangulation_distance, triangulation_angle


def test_triangulation_45_degrees():
    assert triangulation_distance(baseline=2.0, theta_rad=np.deg2rad(45)) == pytest.approx(2.0)


def test_triangulation_round_trip():
    a, theta = 1.5, np.deg2rad(37)
    d = triangulation_distance(a, theta)
    recovered_theta = triangulation_angle(a, d)
    assert recovered_theta == pytest.approx(theta)
