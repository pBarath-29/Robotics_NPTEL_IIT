import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import numpy as np
import pytest
from core.potentiometer import output_voltage, partial_resistance_from_voltage
from core.force_sensor import cantilever_deflection, cantilever_load, apply_calibration_matrix


def test_potentiometer_voltage_divider():
    assert output_voltage(v_in=10, r_partial=250, r_total=1000) == pytest.approx(2.5)


def test_potentiometer_round_trip():
    v_out = output_voltage(v_in=5, r_partial=300, r_total=1200)
    r_recovered = partial_resistance_from_voltage(v_in=5, v_out=v_out, r_total=1200)
    assert r_recovered == pytest.approx(300)


def test_cantilever_round_trip():
    p, l, e, i = 50.0, 0.08, 2.1e11, 4e-10
    delta = cantilever_deflection(p, l, e, i)
    recovered_p = cantilever_load(delta, l, e, i)
    assert recovered_p == pytest.approx(p)


def test_calibration_matrix_identity_like():
    raw = np.array([1, 2, 3, 4, 5, 6, 7, 8], dtype=float)
    cm = np.zeros((6, 8))
    for i in range(6):
        cm[i, i] = 1.0
    result = apply_calibration_matrix(raw, cm)
    assert result == pytest.approx(raw[:6])
