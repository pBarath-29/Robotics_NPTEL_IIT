import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import pytest
from core.kinetic_energy import velocity_outer_product, trace_kinetic_energy, direct_kinetic_energy


def test_trace_form_matches_direct_form():
    vx, vy, vz, dm = 2.0, -1.5, 0.7, 3.0
    assert trace_kinetic_energy(vx, vy, vz, dm) == pytest.approx(direct_kinetic_energy(vx, vy, vz, dm))


def test_outer_product_diagonal_is_squares():
    outer = velocity_outer_product(2.0, 3.0, 4.0)
    assert outer[0, 0] == pytest.approx(4.0)
    assert outer[1, 1] == pytest.approx(9.0)
    assert outer[2, 2] == pytest.approx(16.0)
