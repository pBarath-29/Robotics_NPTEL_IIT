"""Potentiometer position sensor, from Lecture 2.

A voltage divider: Vin/R = Vout/r, where R is the total wire resistance
and r is the partial resistance tapped by the wiper.
"""


def output_voltage(v_in: float, r_partial: float, r_total: float) -> float:
    return v_in * (r_partial / r_total)


def partial_resistance_from_voltage(v_in: float, v_out: float, r_total: float) -> float:
    return (v_out / v_in) * r_total
