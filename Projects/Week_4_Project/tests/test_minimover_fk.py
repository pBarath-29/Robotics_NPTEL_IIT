import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import numpy as np
import pytest
from core.minimover_fk import compute, closed_form_position


def test_dh_chain_matches_closed_form_position():
    l1, l2 = 2.0, 1.5
    thetas = [np.deg2rad(t) for t in [20, 30, 40, 50, 60]]
    t_final, _ = compute(l1, l2, thetas)
    dh_position = t_final[:3, 3]
    expected = closed_form_position(l1, l2, thetas[0], thetas[1], thetas[2])
    assert dh_position == pytest.approx(expected, abs=1e-9)


def test_position_independent_of_theta4_theta5():
    l1, l2 = 2.0, 1.5
    base_thetas = [np.deg2rad(t) for t in [20, 30, 40, 50, 60]]
    other_thetas = [np.deg2rad(t) for t in [20, 30, 40, 999, -123]]
    t1, _ = compute(l1, l2, base_thetas)
    t2, _ = compute(l1, l2, other_thetas)
    assert t1[:3, 3] == pytest.approx(t2[:3, 3], abs=1e-9)


def test_homogeneous_bottom_row():
    t_final, _ = compute(2.0, 1.5, [0.1, 0.2, 0.3, 0.4, 0.5])
    assert t_final[3, :] == pytest.approx([0, 0, 0, 1])
