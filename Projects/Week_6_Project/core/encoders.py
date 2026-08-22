"""Optical encoders, from Lectures 2-3.

Absolute encoders use n concentric rings, each ring one bit, giving 2^n
divisions of the full rotation. Incremental encoders use a single coded
disc and two fixed photo-detectors (A, B); which one enters a dark zone
first reveals the direction of rotation.
"""


def absolute_encoder_divisions(n_rings: int) -> int:
    return 2 ** n_rings


def absolute_encoder_resolution_deg(n_rings: int) -> float:
    return 360.0 / absolute_encoder_divisions(n_rings)


def absolute_encoder_binary_code(angle_deg: float, n_rings: int) -> str:
    """The binary code (one bit per ring) corresponding to a given angle,
    with the outermost ring as the least significant bit (2^0).
    """
    divisions = absolute_encoder_divisions(n_rings)
    step = 360.0 / divisions
    index = int((angle_deg % 360.0) / step)
    return format(index, f"0{n_rings}b")


def incremental_encoder_direction(a_leads_b: bool) -> str:
    """If detector A enters the dark zone before B, rotation is clockwise;
    if B enters first, it is counter-clockwise.
    """
    return "Clockwise" if a_leads_b else "Counter-clockwise"
