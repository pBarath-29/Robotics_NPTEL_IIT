import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import numpy as np
import pytest
from core.boundary_descriptors import (
    DIRECTIONS_4,
    DIRECTIONS_8,
    encode_chain,
    circle_signature,
    square_signature,
    compactness,
    REFERENCE_COMPACTNESS,
    closest_shape_match,
)


def test_chain_code_of_a_unit_square_4_directional():
    # A 1x1 square traced counter-clockwise: right, up, left, down.
    points = [(0, 0), (1, 0), (1, 1), (0, 1)]
    codes = encode_chain(points, DIRECTIONS_4)
    assert codes == [0, 1, 2, 3]


def test_chain_code_handles_multi_unit_segments():
    points = [(0, 0), (3, 0), (3, 1), (0, 1)]
    codes = encode_chain(points, DIRECTIONS_4)
    assert codes == [0, 0, 0, 1, 2, 2, 2, 3]


def test_chain_code_8_directional_diagonal_step():
    # Right triangle: right along x, diagonal back-and-up, then down to close.
    points = [(0, 0), (2, 0), (0, 2)]
    codes = encode_chain(points, DIRECTIONS_8)
    assert codes == [0, 0, 3, 3, 6, 6]


def test_circle_signature_is_constant():
    theta = np.linspace(0, 2 * np.pi, 20)
    r = circle_signature(theta, radius=5.0)
    assert np.allclose(r, 5.0)


def test_square_signature_matches_notes_values():
    # Notes: at theta=0, r=A; at theta=45deg (pi/4), r=A*sqrt(2).
    a = 3.0
    r0 = square_signature(np.array([0.0]), a)[0]
    r45 = square_signature(np.array([np.pi / 4]), a)[0]
    assert r0 == pytest.approx(a)
    assert r45 == pytest.approx(a * np.sqrt(2))


def test_compactness_circle_matches_reference():
    radius = 4.0
    perimeter = 2 * np.pi * radius
    area = np.pi * radius ** 2
    c = compactness(perimeter, area)
    assert c == pytest.approx(REFERENCE_COMPACTNESS["Circle"])


def test_compactness_square_matches_reference():
    side = 5.0
    perimeter = 4 * side
    area = side ** 2
    c = compactness(perimeter, area)
    assert c == pytest.approx(REFERENCE_COMPACTNESS["Square"])


def test_closest_shape_match_identifies_circle():
    measured = 4 * np.pi + 0.01
    assert closest_shape_match(measured) == "Circle"
