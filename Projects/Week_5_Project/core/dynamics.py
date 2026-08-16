"""2-DoF planar manipulator joint torques via the Lagrange-Euler
"Center of Mass" method, from Lecture 6.

Lecture 6 presents this as the practical alternative to the full
matrix-heavy D/h/C term approach (Lectures 2-5): attach the frame to each
link's center of mass, write the kinetic and potential energy directly,
and differentiate the Lagrangian L = K - P using
    tau_i = d/dt(dL/dtheta_i') - dL/dtheta_i
The notes state this is easier to do by hand for a simple 2-DoF or 3-DoF
robot, and that the result is mathematically identical to the full matrix
approach -- which is exactly why it's implemented here rather than the
general D/h/C machinery, which is only practical for much larger robots.

This module builds the Lagrangian symbolically with sympy (matching the
notes' own method of literally differentiating the energy expressions),
so the derivation is exact rather than hand-transcribed.
"""

import numpy as np
import sympy as sp

_t = sp.symbols("t")
_theta1 = sp.Function("theta1")(_t)
_theta2 = sp.Function("theta2")(_t)
_m1, _m2, _l1, _l2, _i1, _i2, _g = sp.symbols("m1 m2 L1 L2 I1 I2 g", positive=True)

_theta1_dot = _theta1.diff(_t)
_theta2_dot = _theta2.diff(_t)
_theta1_ddot = _theta1.diff(_t, 2)
_theta2_ddot = _theta2.diff(_t, 2)

_lc1 = _l1 / 2
_lc2 = _l2 / 2

_x1 = _lc1 * sp.cos(_theta1)
_y1 = _lc1 * sp.sin(_theta1)
_x2 = _l1 * sp.cos(_theta1) + _lc2 * sp.cos(_theta1 + _theta2)
_y2 = _l1 * sp.sin(_theta1) + _lc2 * sp.sin(_theta1 + _theta2)

_v1_sq = sp.diff(_x1, _t) ** 2 + sp.diff(_y1, _t) ** 2
_v2_sq = sp.diff(_x2, _t) ** 2 + sp.diff(_y2, _t) ** 2

_omega1 = _theta1_dot
_omega2 = _theta1_dot + _theta2_dot

_k1 = sp.Rational(1, 2) * _m1 * _v1_sq + sp.Rational(1, 2) * _i1 * _omega1 ** 2
_k2 = sp.Rational(1, 2) * _m2 * _v2_sq + sp.Rational(1, 2) * _i2 * _omega2 ** 2
_k = sp.simplify(_k1 + _k2)

_p1 = -_m1 * _g * _lc1 * sp.sin(_theta1)
_p2 = -_m2 * _g * (_l1 * sp.sin(_theta1) + _lc2 * sp.sin(_theta1 + _theta2))
_p = _p1 + _p2

_lagrangian = _k - _p


def _euler_lagrange(lagrangian, q):
    dq_dt = q.diff(_t)
    d_dt_dl_dqdot = sp.diff(sp.diff(lagrangian, dq_dt), _t)
    dl_dq = sp.diff(lagrangian, q)
    return sp.simplify(d_dt_dl_dqdot - dl_dq)


_tau1_expr = _euler_lagrange(_lagrangian, _theta1)
_tau2_expr = _euler_lagrange(_lagrangian, _theta2)

# Symmetry property stated in the notes: D12 (coefficient of theta2'' in
# tau1) must always equal D21 (coefficient of theta1'' in tau2).
_d12_expr = sp.expand(_tau1_expr).coeff(_theta2_ddot)
_d21_expr = sp.expand(_tau2_expr).coeff(_theta1_ddot)
DYNAMIC_COUPLING_SYMMETRY_HOLDS = sp.simplify(_d12_expr - _d21_expr) == 0

# Substitute plain symbols in place of the time-dependent Function/Derivative
# objects so the expressions can be lambdified into fast numeric functions.
_theta1_s, _theta2_s = sp.symbols("theta1 theta2")
_theta1_dot_s, _theta2_dot_s = sp.symbols("theta1_dot theta2_dot")
_theta1_ddot_s, _theta2_ddot_s = sp.symbols("theta1_ddot theta2_ddot")

_plain_subs = {
    _theta1: _theta1_s, _theta2: _theta2_s,
    _theta1_dot: _theta1_dot_s, _theta2_dot: _theta2_dot_s,
    _theta1_ddot: _theta1_ddot_s, _theta2_ddot: _theta2_ddot_s,
}
_tau1_plain = _tau1_expr.subs(_plain_subs)
_tau2_plain = _tau2_expr.subs(_plain_subs)
_p_plain = _p.subs(_plain_subs)

_args = [_theta1_s, _theta2_s, _theta1_dot_s, _theta2_dot_s,
         _theta1_ddot_s, _theta2_ddot_s, _m1, _m2, _l1, _l2, _i1, _i2, _g]

_tau1_fn = sp.lambdify(_args, _tau1_plain, "numpy")
_tau2_fn = sp.lambdify(_args, _tau2_plain, "numpy")
_potential_energy_fn = sp.lambdify([_theta1_s, _theta2_s, _m1, _m2, _l1, _l2, _g], _p_plain, "numpy")


def compute_torques(theta1, theta2, theta1_dot, theta2_dot, theta1_ddot, theta2_ddot,
                     m1, m2, l1, l2, i1, i2, g=9.81):
    """Returns (tau1, tau2), the joint torques required to produce the
    given joint accelerations at the given state.
    """
    tau1 = float(_tau1_fn(theta1, theta2, theta1_dot, theta2_dot, theta1_ddot, theta2_ddot,
                          m1, m2, l1, l2, i1, i2, g))
    tau2 = float(_tau2_fn(theta1, theta2, theta1_dot, theta2_dot, theta1_ddot, theta2_ddot,
                          m1, m2, l1, l2, i1, i2, g))
    return tau1, tau2


def potential_energy(theta1, theta2, m1, m2, l1, l2, g=9.81):
    return float(_potential_energy_fn(theta1, theta2, m1, m2, l1, l2, g))


def gravity_only_torques(theta1, theta2, m1, m2, l1, l2, i1, i2, g=9.81):
    """Torques with zero velocity and zero acceleration -- should equal
    the gradient of the potential energy (a property of any correctly
    derived Lagrangian, used here to spot-check the symbolic result).
    """
    return compute_torques(theta1, theta2, 0.0, 0.0, 0.0, 0.0, m1, m2, l1, l2, i1, i2, g)
