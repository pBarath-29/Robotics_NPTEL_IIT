import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import pytest
from core.trajectory import cubic_coeffs, quintic_coeffs, poly_eval, parabolic_blend


def test_cubic_matches_worked_case_study():
    # Lecture 5 case study: theta_i=20, theta_f=80, t_f=4 ->
    # theta(t) = 20 + 11.25t^2 - 1.875t^3
    coeffs = cubic_coeffs(20, 80, 4)
    assert coeffs[0] == pytest.approx(20)
    assert coeffs[1] == pytest.approx(0)
    assert coeffs[2] == pytest.approx(11.25)
    assert coeffs[3] == pytest.approx(-1.875)


def test_cubic_boundary_conditions():
    theta_i, theta_f, tf = 10.0, 50.0, 3.0
    coeffs = cubic_coeffs(theta_i, theta_f, tf)
    pos0, vel0, _ = poly_eval(coeffs, 0)
    posf, velf, _ = poly_eval(coeffs, tf)
    assert pos0 == pytest.approx(theta_i)
    assert vel0 == pytest.approx(0)
    assert posf == pytest.approx(theta_f)
    assert velf == pytest.approx(0, abs=1e-9)


def test_quintic_boundary_conditions():
    theta_i, theta_i_dot, theta_i_ddot = 5.0, 1.0, 0.5
    theta_f, theta_f_dot, theta_f_ddot = 40.0, -0.5, 0.2
    tf = 6.0
    coeffs = quintic_coeffs(theta_i, theta_i_dot, theta_i_ddot, theta_f, theta_f_dot, theta_f_ddot, tf)

    pos0, vel0, acc0 = poly_eval(coeffs, 0)
    posf, velf, accf = poly_eval(coeffs, tf)

    assert pos0 == pytest.approx(theta_i)
    assert vel0 == pytest.approx(theta_i_dot)
    assert acc0 == pytest.approx(theta_i_ddot)
    assert posf == pytest.approx(theta_f)
    assert velf == pytest.approx(theta_f_dot)
    assert accf == pytest.approx(theta_f_ddot)


def test_parabolic_blend_matches_worked_case_study():
    # Lecture 5 case study: theta_i=20, theta_f=74, t_f=12, accel=2.0, t_b=3.0
    result = parabolic_blend(20, 74, 12, 2.0, 3.0)
    assert result["theta_a"] == pytest.approx(29)
    assert result["vel_a"] == pytest.approx(6.0)
    assert result["theta_b"] == pytest.approx(65)
    assert result["linear_velocity"] == pytest.approx(6.0)


def test_parabolic_blend_is_self_consistent():
    # For a physically valid blend, the blend-end velocity must equal the
    # constant linear velocity in the middle section. This only holds when
    # theta_f is actually reachable with the given accel/t_b/t_f, so derive
    # a consistent theta_f rather than picking one arbitrarily.
    theta_i, tf, accel, tb = 0.0, 10.0, 3.0, 2.0
    theta_f = theta_i + accel * tb * (tf - tb)
    result = parabolic_blend(theta_i, theta_f, tf, accel, tb)
    assert result["vel_a"] == pytest.approx(result["linear_velocity"])
