"""Grubler's Criterion for manipulator mobility, as taught in Lectures 3-4.

Formulas (lambda = 3 for planar, lambda = 6 for spatial):
    M = lambda * n - sum(lambda - Ci)   over all m joints

Worked examples from the notes, used for verification in tests/test_grubler.py:
    - Planar serial manipulator: n=4, m=4, all Ci=1  -> M = 4
    - Planar parallel manipulator: n=7, m=9, all Ci=1 -> M = 3
    - Stewart Platform (spatial parallel): n=13, 6 legs each with a
      Universal(2) + Prismatic(1) + Spherical(3) joint -> M = 6
"""

from dataclasses import dataclass, field


@dataclass
class MobilityResult:
    mobility: int
    lam: int
    n: int
    joint_constraints: list = field(default_factory=list)
    classification: str = ""
    explanation: str = ""


def compute_mobility(n: int, joint_dofs: list, spatial: bool) -> MobilityResult:
    """Compute mobility M via Grubler's Criterion.

    n: number of moving links.
    joint_dofs: list of connectivity values Ci, one per joint.
    spatial: True for 3D (lambda=6), False for planar (lambda=3).
    """
    lam = 6 if spatial else 3
    total_constraint = sum(lam - ci for ci in joint_dofs)
    mobility = lam * n - total_constraint
    return MobilityResult(
        mobility=mobility,
        lam=lam,
        n=n,
        joint_constraints=[lam - ci for ci in joint_dofs],
    )


def classify_mobility(mobility: int, spatial: bool) -> str:
    """Classify a manipulator as ideal / redundant / under-actuated.

    Ideal DoF requirement: 6 for a spatial manipulator, 3 for a planar one
    (Lecture 3, "Types of Manipulators Based on DoF").
    """
    required = 6 if spatial else 3
    if mobility == required:
        return "Ideal"
    if mobility > required:
        return "Redundant"
    return "Under-actuated"


WORKED_EXAMPLES = {
    "Planar serial manipulator (L3)": {
        "n": 4,
        "joint_dofs": [1, 1, 1, 1],
        "spatial": False,
        "expected_mobility": 4,
    },
    "Planar parallel manipulator (L3)": {
        "n": 7,
        "joint_dofs": [1, 1, 1, 1, 1, 1, 1, 1, 1],
        "spatial": False,
        "expected_mobility": 3,
    },
    "Stewart Platform (L4)": {
        "n": 13,
        # 6 legs, each leg = Universal(2) + Prismatic(1) + Spherical(3)
        "joint_dofs": [2, 1, 3] * 6,
        "spatial": True,
        "expected_mobility": 6,
    },
}
