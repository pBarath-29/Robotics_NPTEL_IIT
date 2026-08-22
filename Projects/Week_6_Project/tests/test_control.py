import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import pytest
from core.control import pd_law, pid_law, simulate_step_response


def test_pd_law_zero_error_gives_only_feedforward():
    result = pd_law(theta_d=10, theta=10, theta_d_dot=0, theta_dot=0, theta_d_ddot=2.5, kp=5, kd=2)
    assert result == pytest.approx(2.5)


def test_pid_law_matches_pd_when_integral_zero():
    pd_result = pd_law(theta_d=10, theta=4, theta_d_dot=0, theta_dot=1, theta_d_ddot=0, kp=3, kd=1)
    pid_result = pid_law(theta_d=10, theta=4, theta_d_dot=0, theta_dot=1, theta_d_ddot=0, e_integral=0, kp=3, ki=7, kd=1)
    assert pd_result == pytest.approx(pid_result)


def test_step_response_converges_to_target():
    t, theta, error = simulate_step_response(theta_d=90, theta0=0, kp=25, kd=8, dt=0.01, t_final=5.0)
    assert abs(error[-1]) < 1.0


def test_step_response_starts_at_initial_condition():
    t, theta, error = simulate_step_response(theta_d=45, theta0=10, kp=10, kd=5, dt=0.01, t_final=1.0)
    assert theta[0] == pytest.approx(10)
    assert t[0] == pytest.approx(0)
