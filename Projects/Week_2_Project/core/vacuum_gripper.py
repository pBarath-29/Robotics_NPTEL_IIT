"""Vacuum gripper physics, from Lecture 2: continuity equation + Bernoulli's equation.

The notes describe the working principle qualitatively: air forced through an
orifice into a venturi tube speeds up (continuity equation), and as velocity
increases, pressure decreases (Bernoulli's equation). The resulting pressure
drop inside the elastic cup, relative to atmospheric pressure outside, holds
a flat object against the cup.
"""

AIR_DENSITY_KG_M3 = 1.225  # standard air density at sea level
GRAVITY_M_S2 = 9.81


def throat_velocity(inlet_velocity: float, inlet_area: float, throat_area: float) -> float:
    """Continuity equation: A1*V1 = A2*V2 -> V2 = V1 * (A1/A2)."""
    return inlet_velocity * (inlet_area / throat_area)


def pressure_drop(inlet_velocity: float, throat_velocity_: float, density: float = AIR_DENSITY_KG_M3) -> float:
    """Bernoulli's equation (same height, incompressible flow):
    P1 + 0.5*rho*V1^2 = P2 + 0.5*rho*V2^2
    Pressure drop (P1 - P2) = 0.5*rho*(V2^2 - V1^2).
    """
    return 0.5 * density * (throat_velocity_ ** 2 - inlet_velocity ** 2)


def lift_force(pressure_drop_pa: float, cup_area_m2: float) -> float:
    """Force holding the object against the cup = pressure differential * cup area."""
    return pressure_drop_pa * cup_area_m2


def can_hold(lift_force_n: float, object_mass_kg: float) -> bool:
    """Whether the vacuum lift force exceeds the object's weight."""
    return lift_force_n >= object_mass_kg * GRAVITY_M_S2
