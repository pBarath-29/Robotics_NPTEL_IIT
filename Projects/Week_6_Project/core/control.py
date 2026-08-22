"""Robot joint control schemes, from Lecture 1.

Partitioned control splits the required torque into two parts:
    tau = alpha * tau' + beta
    alpha = D(theta)                        (inertia terms)
    beta  = h(theta, theta') + C(theta) + F(theta, theta')  (Coriolis, gravity, friction)
tau' is the commanded acceleration from the controller. Because alpha and
beta are chosen to exactly cancel the robot's true dynamics, the closed
loop reduces to a plain double integrator theta'' = tau' -- which is
exactly why the PD/PID law below is written directly in terms of the
desired acceleration, error, and error derivative: substituting
theta'' = tau' into the error dynamics gives
    E'' + Kd*E' + Kp*E = 0    (PD)
a simple, tunable second-order system.

PD:  tau' = theta_d'' + Kp*E + Kd*E'
PID: tau' = theta_d'' + Kp*E + Ki*integral(E dt) + Kd*E'
where E = theta_d - theta.
"""

import numpy as np


def pd_law(theta_d, theta, theta_d_dot, theta_dot, theta_d_ddot, kp, kd):
    e = theta_d - theta
    e_dot = theta_d_dot - theta_dot
    return theta_d_ddot + kp * e + kd * e_dot


def pid_law(theta_d, theta, theta_d_dot, theta_dot, theta_d_ddot, e_integral, kp, ki, kd):
    e = theta_d - theta
    e_dot = theta_d_dot - theta_dot
    return theta_d_ddot + kp * e + ki * e_integral + kd * e_dot


def simulate_step_response(theta_d: float, theta0: float, kp: float, kd: float,
                            ki: float = 0.0, dt: float = 0.01, t_final: float = 5.0):
    """Simulates the closed-loop double-integrator system theta'' = tau'
    tracking a constant (step) target theta_d, using the PID law above.
    Returns arrays of time, theta, and error.
    """
    n = int(t_final / dt) + 1
    t = np.zeros(n)
    theta = np.zeros(n)
    theta_dot = np.zeros(n)
    error = np.zeros(n)

    theta[0] = theta0
    theta_dot[0] = 0.0
    e_integral = 0.0

    for k in range(n - 1):
        e = theta_d - theta[k]
        error[k] = e
        tau_prime = pid_law(theta_d, theta[k], 0.0, theta_dot[k], 0.0, e_integral, kp, ki, kd)
        theta_ddot = tau_prime  # theta'' = tau' under exact partitioned control

        theta_dot[k + 1] = theta_dot[k] + theta_ddot * dt
        theta[k + 1] = theta[k] + theta_dot[k] * dt
        e_integral += e * dt
        t[k + 1] = t[k] + dt

    error[-1] = theta_d - theta[-1]
    return t, theta, error
