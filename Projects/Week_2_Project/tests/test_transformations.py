import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import numpy as np
import pytest
from core.transformations import rot_x, rot_y, rot_z, trans, compose, apply_to_point, invert


def test_rot_z_90_degrees_matches_notes_formula():
    # Rotation about Z by theta: [[cos,-sin,0],[sin,cos,0],[0,0,1]] (Lecture 7).
    # At theta=90deg, cos=0, sin=1, so the X axis point (1,0,0) should land on (0,1,0).
    r = rot_z(np.deg2rad(90))
    p = apply_to_point(r, (1, 0, 0))
    assert p == pytest.approx([0, 1, 0], abs=1e-9)


def test_rot_x_90_degrees_matches_notes_formula():
    r = rot_x(np.deg2rad(90))
    p = apply_to_point(r, (0, 1, 0))
    assert p == pytest.approx([0, 0, 1], abs=1e-9)


def test_rot_y_90_degrees_matches_notes_formula():
    r = rot_y(np.deg2rad(90))
    p = apply_to_point(r, (0, 0, 1))
    assert p == pytest.approx([1, 0, 0], abs=1e-9)


def test_translation_operators_commute():
    # Lecture 7 states: Trans(X, qx) * Trans(Y, qy) = Trans(Y, qy) * Trans(X, qx).
    t_xy = compose([trans(3, 0, 0), trans(0, 5, 0)])
    t_yx = compose([trans(0, 5, 0), trans(3, 0, 0)])
    assert t_xy == pytest.approx(t_yx)


def test_translation_no_rotation_block():
    t = trans(1, 2, 3)
    assert t[:3, :3] == pytest.approx(np.eye(3))
    assert t[:3, 3] == pytest.approx([1, 2, 3])


def test_compose_then_invert_is_identity():
    combined = compose([trans(2, -1, 4), rot_z(np.deg2rad(37)), rot_x(np.deg2rad(-15))])
    inv = invert(combined)
    check = combined @ inv
    assert check == pytest.approx(np.eye(4), abs=1e-9)


def test_homogeneous_bottom_row():
    for m in [trans(1, 2, 3), rot_x(0.5), rot_y(0.5), rot_z(0.5)]:
        assert m[3, :] == pytest.approx([0, 0, 0, 1])
