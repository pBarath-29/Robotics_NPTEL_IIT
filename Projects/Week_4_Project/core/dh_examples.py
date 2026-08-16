"""Additional DH parameter assignment examples, from Lecture 3."""

import numpy as np

DH_EXAMPLES = {
    "T-S-R (Twisting-Sliding-Revolute)": {
        "description": "3-DoF serial manipulator. Sequence: Twisting -> Sliding -> Revolute.",
        "rows": [
            {"name": "1 (Twisting)", "theta_variable": True, "theta_fixed_deg": None,
             "d_variable": False, "d_fixed": "a* (fixed)", "alpha_deg": 0, "a": 0},
            {"name": "2 (Sliding)", "theta_variable": False, "theta_fixed_deg": 0,
             "d_variable": True, "d_fixed": None, "alpha_deg": -90, "a": 0},
            {"name": "3 (Revolute)", "theta_variable": True, "theta_fixed_deg": None,
             "d_variable": False, "d_fixed": 0, "alpha_deg": 0, "a": "c"},
        ],
    },
    "S-T-R (Sliding-Twisting-Revolute)": {
        "description": "3-DoF serial manipulator. Sequence: Sliding -> Twisting -> Revolute.",
        "rows": [
            {"name": "1 (Sliding)", "theta_variable": False, "theta_fixed_deg": 0,
             "d_variable": True, "d_fixed": None, "alpha_deg": 0, "a": 0},
            {"name": "2 (Twisting)", "theta_variable": True, "theta_fixed_deg": None,
             "d_variable": False, "d_fixed": "b* (fixed)", "alpha_deg": -90, "a": 0},
            {"name": "3 (Revolute)", "theta_variable": True, "theta_fixed_deg": None,
             "d_variable": False, "d_fixed": 0, "alpha_deg": 0, "a": "c"},
        ],
    },
}


def build_numeric_dh_table(example_name: str, theta_values_deg: dict, d_values: dict, a_c_value: float):
    """Build a numeric DH table for one of the examples above, given values
    for whichever parameters are variable in that example, so the generic
    forward-kinematics engine can be run on it.
    """
    rows = DH_EXAMPLES[example_name]["rows"]
    table = []
    for i, row in enumerate(rows):
        theta = np.deg2rad(theta_values_deg.get(i, 0)) if row["theta_variable"] else np.deg2rad(row["theta_fixed_deg"])
        d = d_values.get(i, 0) if row["d_variable"] else (row["d_fixed"] if isinstance(row["d_fixed"], (int, float)) else d_values.get(i, 0))
        alpha = np.deg2rad(row["alpha_deg"])
        a = a_c_value if row["a"] == "c" else row["a"]
        table.append({"theta": theta, "d": d, "alpha": alpha, "a": a})
    return table
