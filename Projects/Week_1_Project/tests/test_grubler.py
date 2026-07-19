import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import pytest
from core.grubler import compute_mobility, classify_mobility, WORKED_EXAMPLES


@pytest.mark.parametrize("name,data", WORKED_EXAMPLES.items())
def test_worked_examples_match_notes(name, data):
    result = compute_mobility(
        n=data["n"], joint_dofs=data["joint_dofs"], spatial=data["spatial"]
    )
    assert result.mobility == data["expected_mobility"], (
        f"{name}: expected M={data['expected_mobility']}, got {result.mobility}"
    )


def test_planar_serial_is_redundant():
    result = compute_mobility(n=4, joint_dofs=[1, 1, 1, 1], spatial=False)
    assert classify_mobility(result.mobility, spatial=False) == "Redundant"


def test_planar_parallel_is_ideal():
    result = compute_mobility(n=7, joint_dofs=[1] * 9, spatial=False)
    assert classify_mobility(result.mobility, spatial=False) == "Ideal"


def test_stewart_platform_is_ideal_spatial():
    result = compute_mobility(n=13, joint_dofs=[2, 1, 3] * 6, spatial=True)
    assert result.mobility == 6
    assert classify_mobility(result.mobility, spatial=True) == "Ideal"


def test_under_actuated_classification():
    # 3 moving links, 3 revolute joints in a spatial context -> M=3 < 6
    result = compute_mobility(n=3, joint_dofs=[1, 1, 1], spatial=True)
    assert classify_mobility(result.mobility, spatial=True) == "Under-actuated"
