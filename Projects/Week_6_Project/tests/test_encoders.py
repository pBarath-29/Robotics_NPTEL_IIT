import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import pytest
from core.encoders import (
    absolute_encoder_divisions,
    absolute_encoder_resolution_deg,
    absolute_encoder_binary_code,
    incremental_encoder_direction,
)


def test_divisions_match_notes_examples():
    assert absolute_encoder_divisions(4) == 16
    assert absolute_encoder_divisions(10) == 1024


def test_resolution_matches_notes_worked_example():
    # Notes: with n=10 rings, resolution = 360/1024 = 0.35 deg/step.
    assert absolute_encoder_resolution_deg(10) == pytest.approx(0.3515625)
    assert round(absolute_encoder_resolution_deg(10), 2) == pytest.approx(0.35)


def test_binary_code_length_matches_ring_count():
    code = absolute_encoder_binary_code(45.0, 4)
    assert len(code) == 4


def test_binary_code_zero_degrees_is_all_zeros():
    assert absolute_encoder_binary_code(0.0, 4) == "0000"


def test_incremental_direction():
    assert incremental_encoder_direction(True) == "Clockwise"
    assert incremental_encoder_direction(False) == "Counter-clockwise"
