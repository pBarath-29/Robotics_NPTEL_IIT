import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import numpy as np
import pytest
from core.dh import forward_kinematics
from core.dh_examples import DH_EXAMPLES, build_numeric_dh_table


def test_both_examples_build_and_run():
    for name in DH_EXAMPLES:
        table = build_numeric_dh_table(name, {0: 15, 2: 25}, {1: 4.0}, 3.0)
        t_final, frames = forward_kinematics(table)
        assert len(frames) == 4
        assert np.all(np.isfinite(t_final))
        assert t_final[3, :] == pytest.approx([0, 0, 0, 1])


def test_tsr_table_has_three_rows():
    assert len(DH_EXAMPLES["T-S-R (Twisting-Sliding-Revolute)"]["rows"]) == 3


def test_str_table_has_three_rows():
    assert len(DH_EXAMPLES["S-T-R (Sliding-Twisting-Revolute)"]["rows"]) == 3
