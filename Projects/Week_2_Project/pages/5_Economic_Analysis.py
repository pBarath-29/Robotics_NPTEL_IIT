import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import streamlit as st
from core.economics import full_analysis

st.set_page_config(page_title="Economic Analysis", page_icon="💰", layout="wide")
st.title("💰 Economic Analysis")

st.markdown(
    "Work out whether buying a robot on a bank loan pays off, using the "
    "same formulas and steps as the case study in the notes."
)

if "econ_defaults" not in st.session_state:
    st.session_state.econ_defaults = {
        # A realistic Singapore scenario: a mid-range industrial robot in SGD,
        # Singapore's flat 17% corporate tax rate, and a typical SME business
        # loan rate (rather than the notes' Indian Rupee figures and ~10% rate).
        "asset_cost": 180_000,
        "installation_cost": 40_000,
        "labor_savings_rate": 18,
        "material_savings_rate": 4,
        "operating_rate": 8,
        "running_hours": 4000,
        "life_years": 6,
        "tax_rate_pct": 17,
        "bank_interest_rate": 5,
    }

st.caption(
    "Defaults above reflect a realistic Singapore scenario: SGD costs, "
    "Singapore's 17% corporate tax rate, and a typical SME loan rate."
)

d = st.session_state.econ_defaults

col1, col2 = st.columns(2)
with col1:
    asset_cost = st.number_input("Cost of robot (S$)", min_value=0, value=int(d["asset_cost"]), step=10000)
    installation_cost = st.number_input("Installation cost (S$)", min_value=0, value=int(d["installation_cost"]), step=10000)
    labor_savings_rate = st.number_input("Labor savings (S$/hour)", min_value=0.0, value=float(d["labor_savings_rate"]))
    material_savings_rate = st.number_input("Material savings (S$/hour)", min_value=0.0, value=float(d["material_savings_rate"]))
    operating_rate = st.number_input("Operating/maintenance cost (S$/hour)", min_value=0.0, value=float(d["operating_rate"]))
with col2:
    running_hours = st.number_input("Running hours per year", min_value=1, value=int(d["running_hours"]))
    life_years = st.number_input("Techno-economic life (years)", min_value=1, value=int(d["life_years"]))
    tax_rate_pct = st.number_input("Tax rate (%)", min_value=0.0, max_value=100.0, value=float(d["tax_rate_pct"]))
    bank_interest_rate = st.number_input("Bank interest rate (%)", min_value=0.0, value=float(d["bank_interest_rate"]))

result = full_analysis(
    asset_cost=asset_cost,
    installation_cost=installation_cost,
    labor_savings_rate=labor_savings_rate,
    material_savings_rate=material_savings_rate,
    operating_rate=operating_rate,
    running_hours=running_hours,
    life_years=life_years,
    tax_rate=tax_rate_pct / 100,
)

st.divider()
st.subheader("Results")

c1, c2, c3, c4 = st.columns(4)
c1.metric("F (Capital Investment)", f"S$ {result.f:,.0f}")
c2.metric("B (Annual Savings)", f"S$ {result.b:,.0f}")
c3.metric("C (Operating Cost)", f"S$ {result.c:,.0f}")
c4.metric("D (Depreciation)", f"S$ {result.d:,.0f}")

c5, c6, c7 = st.columns(3)
c5.metric("Net Savings (A)", f"S$ {result.net_savings:,.0f}")
c6.metric("G (Tax)", f"S$ {result.g:,.0f}")
c7.metric("I (Modified Net Savings)", f"S$ {result.i:,.0f}")

c8, c9 = st.columns(2)
c8.metric("E (Payback Period)", f"{result.e:.2f} years")
c9.metric("H (Rate of Return)", f"{result.h:.2f} %")

st.divider()
favorable = result.e < life_years and result.h > bank_interest_rate
if favorable:
    st.success(
        f"Payback period ({result.e:.2f} years) is less than the techno-economic "
        f"life ({life_years} years), and the rate of return ({result.h:.2f}%) is "
        f"greater than the bank interest rate ({bank_interest_rate}%). "
        f"The purchase looks financially favorable."
    )
else:
    st.warning(
        f"Payback period ({result.e:.2f} years) vs. life ({life_years} years), "
        f"rate of return ({result.h:.2f}%) vs. bank interest rate ({bank_interest_rate}%). "
        f"At least one condition is not met, so the purchase does not clearly pay off."
    )
