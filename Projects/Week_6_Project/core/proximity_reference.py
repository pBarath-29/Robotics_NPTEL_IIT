"""Proximity sensor types, from Lecture 4."""

PROXIMITY_SENSORS = {
    "Inductive": {
        "target_material": "Strictly ferromagnetic materials.",
        "principle": (
            "A permanent magnet generates constant magnetic flux. An "
            "approaching ferromagnetic object deflects the field, inducing "
            "a voltage/current in surrounding coils. The induced voltage "
            "amplitude depends on the object's approach speed."
        ),
    },
    "Hall-Effect": {
        "target_material": "Strictly ferromagnetic materials.",
        "principle": (
            "Based on the Lorentz force F = q(V x B). A semiconductor "
            "between magnet poles has a baseline voltage from the magnetic "
            "field. An approaching ferromagnetic object absorbs/redirects "
            "field lines, dropping the field strength and the induced "
            "voltage proportionally."
        ),
    },
    "Capacitive": {
        "target_material": "Any material, magnetic or non-magnetic.",
        "principle": (
            "A sensitive electrode accumulates static charge near any "
            "approaching object, changing its capacitance. Past a "
            "threshold, the electrode oscillates relative to a fixed "
            "reference ring, and a PCB converts the oscillations into an "
            "output voltage correlated with distance."
        ),
    },
}
