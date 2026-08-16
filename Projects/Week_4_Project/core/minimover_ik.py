"""Inverse kinematics of the MINIMOVER 5-DoF manipulator, from Lecture 2.

Given a target position (qx, qy, qz) and orientation matrix R (the top-left
3x3 of the target T_5_0), solve for the 5 joint angles in sequence:

  theta1 = atan2(qy, qx)
  theta3 = acos[(qx^2+qy^2+qz^2 - L1^2 - L2^2) / (2*L1*L2)]     (two solutions, +-)
  theta2: solved from the position equations once theta1, theta3 are known
          (see the derivation below -- a linear system in cos(theta2),
          sin(theta2), solved directly rather than via the notes'
          abbreviated rho/alpha substitution, for a fully closed form).
  theta4: from tan(theta2+theta3+theta4) = (r13*cos1 + r23*sin1) / r33
  theta5: from the remaining orientation elements

Position equations (Lecture 1):
    s  = L1*cos(theta2) + L2*cos(theta2+theta3)   (= sqrt(qx^2+qy^2))
    -qz = L1*sin(theta2) + L2*sin(theta2+theta3)
Expanding cos(theta2+theta3) and sin(theta2+theta3) turns this into a
linear system for [cos(theta2), sin(theta2)] with
    A = L1 + L2*cos(theta3),  B = L2*sin(theta3)
    s   = A*cos(theta2) - B*sin(theta2)
    -qz = B*cos(theta2) + A*sin(theta2)
which inverts directly to:
    cos(theta2) = (A*s - B*qz) / (A^2 + B^2)
    sin(theta2) = (-B*s - A*qz) / (A^2 + B^2)
"""

import numpy as np


class UnreachableTarget(Exception):
    pass


def solve_position(l1: float, l2: float, qx: float, qy: float, qz: float):
    """Returns a list of up to two (theta1, theta2, theta3, label) solutions."""
    theta1 = np.arctan2(qy, qx)

    d_sq = qx ** 2 + qy ** 2 + qz ** 2
    cos_theta3 = (d_sq - l1 ** 2 - l2 ** 2) / (2 * l1 * l2)
    if cos_theta3 < -1 - 1e-9 or cos_theta3 > 1 + 1e-9:
        raise UnreachableTarget(
            f"Target ({qx}, {qy}, {qz}) is out of reach for L1={l1}, L2={l2}."
        )
    cos_theta3 = np.clip(cos_theta3, -1.0, 1.0)

    s = np.sqrt(qx ** 2 + qy ** 2)
    solutions = []
    for sign, label in [(1, "Elbow solution A"), (-1, "Elbow solution B")]:
        theta3 = sign * np.arccos(cos_theta3)
        a = l1 + l2 * np.cos(theta3)
        b = l2 * np.sin(theta3)
        denom = a ** 2 + b ** 2
        cos_theta2 = (a * s - b * qz) / denom
        sin_theta2 = (-b * s - a * qz) / denom
        theta2 = np.arctan2(sin_theta2, cos_theta2)
        solutions.append((theta1, theta2, theta3, label))
    return solutions


def solve_wrist(theta1: float, theta2: float, theta3: float, r: np.ndarray):
    """Given theta1-3 and the target 3x3 orientation matrix R, solve theta4, theta5."""
    r13, r23, r33 = r[0, 2], r[1, 2], r[2, 2]
    numerator_4 = r13 * np.cos(theta1) + r23 * np.sin(theta1)
    theta234 = np.arctan2(numerator_4, r33)
    theta4 = theta234 - theta2 - theta3

    r11, r21, r12, r22 = r[0, 0], r[1, 0], r[0, 1], r[1, 1]
    num5 = -r11 * np.sin(theta1) + r21 * np.cos(theta1)
    den5 = -r12 * np.sin(theta1) + r22 * np.cos(theta1)
    theta5 = np.arctan2(num5, den5)
    return theta4, theta5


def solve_full(l1: float, l2: float, qx: float, qy: float, qz: float, r: np.ndarray):
    """Full 5-DoF IK: position solutions each paired with the wrist angles."""
    results = []
    for theta1, theta2, theta3, label in solve_position(l1, l2, qx, qy, qz):
        theta4, theta5 = solve_wrist(theta1, theta2, theta3, r)
        results.append((theta1, theta2, theta3, theta4, theta5, label))
    return results
