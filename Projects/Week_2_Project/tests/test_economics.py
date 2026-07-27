import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import pytest
from core.economics import full_analysis, WORKED_EXAMPLE


def test_worked_example_matches_notes():
    w = WORKED_EXAMPLE
    result = full_analysis(
        asset_cost=w["asset_cost"],
        installation_cost=w["installation_cost"],
        labor_savings_rate=w["labor_savings_rate"],
        material_savings_rate=w["material_savings_rate"],
        operating_rate=w["operating_rate"],
        running_hours=w["running_hours"],
        life_years=w["life_years"],
        tax_rate=w["tax_rate"],
    )

    assert result.f == w["expected_f"]
    assert result.b == w["expected_b"]
    assert result.c == w["expected_c"]
    assert result.d == w["expected_d"]
    assert result.net_savings == w["expected_net_savings"]
    assert result.g == w["expected_g"]
    assert result.i == w["expected_i"]
    assert result.h == pytest.approx(w["expected_h"], abs=0.01)

    # The notes state E = 3.9 years. The precise formula gives about 3.956
    # years; the notes' figure is a truncation to one decimal place, not a
    # standard rounding. Check both: the precise math, and that truncating
    # our result the same way reproduces the notes' stated figure.
    assert result.e == pytest.approx(1_500_000 / 379_200, rel=1e-9)
    truncated = int(result.e * 10) / 10
    assert truncated == 3.9


def test_favorable_purchase_condition():
    w = WORKED_EXAMPLE
    result = full_analysis(
        asset_cost=w["asset_cost"],
        installation_cost=w["installation_cost"],
        labor_savings_rate=w["labor_savings_rate"],
        material_savings_rate=w["material_savings_rate"],
        operating_rate=w["operating_rate"],
        running_hours=w["running_hours"],
        life_years=w["life_years"],
        tax_rate=w["tax_rate"],
    )
    assert result.e < w["life_years"]
    assert result.h > w["bank_interest_rate"]
