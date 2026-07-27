"""Economic analysis of a robot purchase, from Lecture 4 (formulas) and
Lecture 5 (worked case study).

Formulas, exactly as given in the notes:
    F = Capital Investment (asset cost + installation cost)
    B = Annual Savings = (labor savings rate + material savings rate) * running hours
    C = Annual Operating Cost = operating rate * running hours
    D = Depreciation = asset cost / techno-economic life (applies to asset cost only,
        excluding installation, per the Lecture 5 case study)
    Net Savings (A) = B - C - D
    G = Tax = tax rate * Net Savings
    I = Modified Net Savings = Net Savings - G
    E = Payback Period = F / (B - C - G)
    H = Rate of Return on Investment = (I / F) * 100
"""

from dataclasses import dataclass


def capital_investment(asset_cost: float, installation_cost: float) -> float:
    return asset_cost + installation_cost


def annual_savings(labor_savings_rate: float, material_savings_rate: float, running_hours: float) -> float:
    return (labor_savings_rate + material_savings_rate) * running_hours


def annual_operating_cost(operating_rate: float, running_hours: float) -> float:
    return operating_rate * running_hours


def depreciation(asset_cost: float, life_years: float) -> float:
    return asset_cost / life_years


def net_savings(b: float, c: float, d: float) -> float:
    return b - c - d


def tax(net_savings_value: float, tax_rate: float) -> float:
    return tax_rate * net_savings_value


def modified_net_savings(net_savings_value: float, tax_value: float) -> float:
    return net_savings_value - tax_value


def payback_period(f: float, b: float, c: float, g: float) -> float:
    return f / (b - c - g)


def rate_of_return(i: float, f: float) -> float:
    return (i / f) * 100


@dataclass
class EconomicAnalysisResult:
    f: float
    b: float
    c: float
    d: float
    net_savings: float
    g: float
    i: float
    e: float
    h: float


def full_analysis(asset_cost, installation_cost, labor_savings_rate, material_savings_rate,
                   operating_rate, running_hours, life_years, tax_rate) -> EconomicAnalysisResult:
    f = capital_investment(asset_cost, installation_cost)
    b = annual_savings(labor_savings_rate, material_savings_rate, running_hours)
    c = annual_operating_cost(operating_rate, running_hours)
    d = depreciation(asset_cost, life_years)
    ns = net_savings(b, c, d)
    g = tax(ns, tax_rate)
    i = modified_net_savings(ns, g)
    e = payback_period(f, b, c, g)
    h = rate_of_return(i, f)
    return EconomicAnalysisResult(f=f, b=b, c=c, d=d, net_savings=ns, g=g, i=i, e=e, h=h)


# Lecture 5's worked case study, used both to pre-fill the UI and to verify
# the formulas above reproduce the same numbers.
WORKED_EXAMPLE = {
    "asset_cost": 1_200_000,
    "installation_cost": 300_000,
    "labor_savings_rate": 100,
    "material_savings_rate": 15,
    "operating_rate": 20,
    "running_hours": 24 * 200,  # 4,800 hours/year
    "life_years": 6,
    "tax_rate": 0.30,
    "bank_interest_rate": 10,
    # Values as stated in the notes (E is rounded/truncated there to 1 decimal).
    "expected_f": 1_500_000,
    "expected_b": 552_000,
    "expected_c": 96_000,
    "expected_d": 200_000,
    "expected_net_savings": 256_000,
    "expected_g": 76_800,
    "expected_i": 179_200,
    "expected_h": 11.95,
}
