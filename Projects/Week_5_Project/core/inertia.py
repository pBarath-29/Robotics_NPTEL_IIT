"""Inertia tensors for robot links, from Lectures 1-2.

Both link shapes use a coordinate frame at the motor end of the link
(not the center of mass), since dynamic control is based on the reaction
torque felt at the motor.

Rectangular link (sides a, b; length l):
    Ixx = (m/12) * (4*l^2 + b^2)
    Iyy = (m/12) * (a^2 + b^2)
    Izz = (m/12) * (4*l^2 + a^2)
    Center of mass at y = -l/2. All products of inertia are 0.

Circular link (radius r; length l):
    Ixx = (1/2) * m * r^2
    Iyy = (m*l^2/3) + (m*r^2/4)
    Izz = (m*l^2/3) + (m*r^2/4)
    Center of mass at x = -l/2. All products of inertia are 0.

Lecture 6 shifts the frame to the center of mass via the Parallel Axis
Theorem: I_zz(center) = I_zz(base) - m*(xbar^2 + ybar^2).
"""

from dataclasses import dataclass


@dataclass
class InertiaTensor:
    ixx: float
    iyy: float
    izz: float
    center_of_mass: tuple


def rectangular_inertia_tensor(m: float, a: float, b: float, l: float) -> InertiaTensor:
    ixx = (m / 12) * (4 * l ** 2 + b ** 2)
    iyy = (m / 12) * (a ** 2 + b ** 2)
    izz = (m / 12) * (4 * l ** 2 + a ** 2)
    return InertiaTensor(ixx=ixx, iyy=iyy, izz=izz, center_of_mass=(0.0, -l / 2, 0.0))


def circular_inertia_tensor(m: float, r: float, l: float) -> InertiaTensor:
    ixx = 0.5 * m * r ** 2
    iyy = (m * l ** 2) / 3 + (m * r ** 2) / 4
    izz = (m * l ** 2) / 3 + (m * r ** 2) / 4
    return InertiaTensor(ixx=ixx, iyy=iyy, izz=izz, center_of_mass=(-l / 2, 0.0, 0.0))


def parallel_axis_shift_izz(izz_base: float, m: float, x_bar: float, y_bar: float) -> float:
    """Shift Izz from the base (motor-end) frame to the center of mass."""
    return izz_base - m * (x_bar ** 2 + y_bar ** 2)


def circular_center_of_mass_izz(m: float, r: float, l: float) -> float:
    """Closed form given directly in Lecture 6: Izz(c) = (1/12)*m*l^2 + (1/4)*m*r^2."""
    return (1 / 12) * m * l ** 2 + (1 / 4) * m * r ** 2


def rectangular_center_of_mass_izz(m: float, a: float, l: float) -> float:
    """Derived the same way as the circular case (Parallel Axis Theorem
    applied to the Lecture 1 rectangular Izz), not given explicitly in the
    notes but following the identical method Lecture 6 uses for the
    circular link.
    """
    base = rectangular_inertia_tensor(m, a, 0, l)
    _, y_bar, _ = base.center_of_mass
    return parallel_axis_shift_izz(base.izz, m, 0.0, y_bar)
