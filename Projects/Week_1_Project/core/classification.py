"""Robot classification taxonomy from Lecture 4:
"Manipulator Mobility, Classification & Workspace".

Classifies a serial manipulator by its 3-joint coordinate-system pattern,
and provides the task-type / controller-type explainer text from the
same lecture.
"""

COORDINATE_SYSTEMS = {
    "Cartesian": {
        "patterns": ["PPP", "SSS"],
        "description": (
            "3 independent linear movements (X, Y, Z). Highly rigid and "
            "accurate, ideal for pick-and-place floor operations."
        ),
        "examples": ["IBM RS-1", "Sigma (Olivetti)"],
        "workspace_shape": "Cuboid",
    },
    "Cylindrical": {
        "patterns": ["TSS", "TPP", "TSP", "TPS"],
        "description": (
            "2 linear joints and 1 rotary (twisting) joint. Restricted "
            "vertical/horizontal reach near the base and poor dynamic "
            "performance due to the rotary joint."
        ),
        "examples": ["Versatran 600"],
        "workspace_shape": "Cylindrical annular space",
    },
    "Spherical / Polar": {
        "patterns": ["TRS", "TRP"],
        "description": (
            "1 linear joint and 2 rotary joints. Useful for picking objects "
            "off the floor, shares dynamic performance limitations with "
            "cylindrical robots."
        ),
        "examples": ["Unimate 2000B"],
        "workspace_shape": "Swept spherical profile",
    },
    "Revolute / Articulated": {
        "patterns": ["TRR"],
        "description": (
            "3 rotary joints (TRR). Highly versatile and widely used in "
            "industry for drilling, milling, etc."
        ),
        "examples": ["PUMA", "T3", "CRS"],
        "workspace_shape": "Intersecting partial spheres",
    },
}

TASK_TYPES = {
    "Point-to-Point": (
        "The tool is withdrawn from the job between tasks (e.g. drilling "
        "holes at specified locations). Examples: Unimate 2000, T3."
    ),
    "Continuous Path": (
        "The tool remains continuously in touch with the job (e.g. tracing "
        "a complex profile with a milling cutter). Examples: PUMA, CRS. "
        "A continuous path robot can perform point-to-point tasks, but not "
        "the reverse."
    ),
}

CONTROLLER_TYPES = {
    "Non-Servo-Controlled": (
        "Open-loop control system, no feedback loop. Errors are not "
        "measured or compensated for. Less accurate, less expensive. "
        "Example: Seiko PN-100."
    ),
    "Servo-Controlled": (
        "Closed-loop control system. Output is measured, compared to the "
        "input, and the resulting error is fed back to the controller. "
        "Highly accurate, more expensive. Examples: Unimate 2000, PUMA, T3."
    ),
}


def classify_sequence(sequence: str):
    """Match a joint-letter sequence (e.g. 'TRR') to a coordinate system.

    Returns the matching system name and its data dict, or None if no
    3-joint serial pattern in the L4 taxonomy matches.
    """
    seq = sequence.strip().upper()
    for system, data in COORDINATE_SYSTEMS.items():
        if seq in data["patterns"]:
            return system, data
    return None, None
