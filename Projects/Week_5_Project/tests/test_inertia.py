import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import pytest
from core.inertia import (
    rectangular_inertia_tensor,
    circular_inertia_tensor,
    parallel_axis_shift_izz,
    circular_center_of_mass_izz,
    rectangular_center_of_mass_izz,
)


def test_rectangular_formulas_match_notes():
    m, a, b, l = 4.0, 0.2, 0.3, 1.5
    t = rectangular_inertia_tensor(m, a, b, l)
    assert t.ixx == pytest.approx((m / 12) * (4 * l ** 2 + b ** 2))
    assert t.iyy == pytest.approx((m / 12) * (a ** 2 + b ** 2))
    assert t.izz == pytest.approx((m / 12) * (4 * l ** 2 + a ** 2))
    assert t.center_of_mass == (0.0, -l / 2, 0.0)


def test_circular_formulas_match_notes():
    m, r, l = 4.0, 0.1, 1.5
    t = circular_inertia_tensor(m, r, l)
    assert t.ixx == pytest.approx(0.5 * m * r ** 2)
    assert t.iyy == pytest.approx((m * l ** 2) / 3 + (m * r ** 2) / 4)
    assert t.izz == pytest.approx((m * l ** 2) / 3 + (m * r ** 2) / 4)
    assert t.center_of_mass == (-l / 2, 0.0, 0.0)


def test_circular_center_of_mass_izz_matches_lecture6_closed_form():
    m, r, l = 3.0, 0.08, 1.2
    base = circular_inertia_tensor(m, r, l)
    x_bar, y_bar, _ = base.center_of_mass
    shifted = parallel_axis_shift_izz(base.izz, m, x_bar, y_bar)
    expected = circular_center_of_mass_izz(m, r, l)
    assert shifted == pytest.approx(expected)
    # Direct closed form from Lecture 6.
    assert expected == pytest.approx((1 / 12) * m * l ** 2 + (1 / 4) * m * r ** 2)


def test_rectangular_center_of_mass_izz_is_self_consistent():
    m, a, l = 3.0, 0.15, 1.2
    base = rectangular_inertia_tensor(m, a, 0, l)
    x_bar, y_bar, _ = base.center_of_mass
    shifted = parallel_axis_shift_izz(base.izz, m, x_bar, y_bar)
    assert shifted == pytest.approx(rectangular_center_of_mass_izz(m, a, l))
    # Reduces to the standard thin-rod-about-center formula.
    assert shifted == pytest.approx((m / 12) * (l ** 2 + a ** 2))


def test_slender_link_approximation_removes_cross_section_terms():
    m, l = 2.0, 1.0
    slender = circular_inertia_tensor(m, r=0.0, l=l)
    assert slender.iyy == pytest.approx((m * l ** 2) / 3)
    assert slender.ixx == pytest.approx(0.0)
