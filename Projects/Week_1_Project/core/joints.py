"""Joint type reference data, as introduced in Lectures 1-3.

Source: Week 1, "Introduction to Robots and Robotics" (L1) and
"Robotic System Components & Joints" (L2), "Kinematic Diagrams & DoF" (L3).
"""

JOINTS = {
    "R": {
        "name": "Revolute",
        "category": "Rotary",
        "dof": 1,
        "description": (
            "Axis of rotation is at 90 degrees to the axis of the output link. "
            "The variable is the joint angle (theta)."
        ),
        "analogy": "Tilting your head up and down.",
    },
    "P": {
        "name": "Prismatic",
        "category": "Linear",
        "dof": 1,
        "description": (
            "Sliding motion where one part translates strictly along a linear "
            "direction, like inserting a key into a block. Joint angle is fixed."
        ),
        "analogy": "A drawer sliding in and out.",
    },
    "S": {
        "name": "Sliding",
        "category": "Linear",
        "dof": 1,
        "description": (
            "Strictly linear movement, similar to a pin inserted into a block, "
            "locking movement to a single sliding path."
        ),
        "analogy": "A pin sliding through a guide block.",
    },
    "T": {
        "name": "Twisting",
        "category": "Rotary",
        "dof": 1,
        "description": (
            "Axis of rotation coincides with the axis of the output link."
        ),
        "analogy": "Shaking your head left and right, or turning a screwdriver.",
    },
    "C": {
        "name": "Cylindrical",
        "category": "Compound (Linear + Rotary)",
        "dof": 2,
        "description": (
            "Combination of one linear and one rotary movement — the link can "
            "slide up/down and rotate. Variables: theta_j (rotation) and "
            "d_j (linear displacement)."
        ),
        "analogy": "A screw-top jar lid being twisted while sliding up.",
    },
    "U": {
        "name": "Hooke / Universal",
        "category": "Compound (Rotary + Rotary)",
        "dof": 2,
        "description": (
            "Formed by combining two revolute joints. Commonly used in "
            "parallel manipulators, not serial."
        ),
        "analogy": "A car's universal joint / drive shaft coupling.",
    },
    "S'": {
        "name": "Spherical / Ball-and-Socket",
        "category": "Compound (Rotary x3)",
        "dof": 3,
        "description": (
            "Allows rotation across 3 axes (X, Y, Z). Used exclusively in "
            "parallel manipulators."
        ),
        "analogy": "A human shoulder or hip joint.",
    },
}


def get_joint(symbol: str) -> dict:
    """Look up a joint by its kinematic-diagram symbol."""
    return JOINTS[symbol]


def joint_symbols() -> list:
    return list(JOINTS.keys())
