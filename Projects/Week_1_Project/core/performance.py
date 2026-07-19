"""Performance specification calculators from Lecture 5:
resolution (BRU / control resolution), accuracy, and repeatability.
"""

import numpy as np
import matplotlib.pyplot as plt

# 1 BRU examples given in the notes: 0.01 inch, 0.001 mm, or 0.1 degree.
BRU_UNIT_PRESETS = {
    "0.01 inch": 0.01,
    "0.001 mm": 0.001,
    "0.1 degree": 0.1,
}


def control_resolution_deg(pulses_per_revolution: float) -> float:
    """Control resolution from an optical encoder's pulses-per-revolution.

    Notes example: 1000 pulses per 360-degree rotation -> 0.36 deg/pulse.
    """
    return 360.0 / pulses_per_revolution


def programming_resolution(bru_value: float, num_brus: int) -> float:
    """Smallest programmable increment given a BRU size and a count of BRUs."""
    return bru_value * num_brus


def accuracy_repeatability_demo(target, accuracy_offset, repeatability_std, n_attempts=20, seed=42):
    """Illustrative scatter plot distinguishing accuracy from repeatability.

    target: (x, y) theoretical commanded point.
    accuracy_offset: (dx, dy) constant systematic offset of the "true mean"
        landing point from the target (this distance is the accuracy).
    repeatability_std: standard deviation of scatter around that mean
        landing point across repeated attempts (this spread is the
        repeatability), matching the L5 definitions exactly.
    """
    rng = np.random.default_rng(seed)
    mean_point = (target[0] + accuracy_offset[0], target[1] + accuracy_offset[1])
    xs = rng.normal(mean_point[0], repeatability_std, n_attempts)
    ys = rng.normal(mean_point[1], repeatability_std, n_attempts)

    fig, ax = plt.subplots(figsize=(5, 5))
    ax.scatter(xs, ys, color="tab:red", alpha=0.7, label=f"{n_attempts} repeated attempts")
    ax.scatter(*target, color="black", marker="x", s=120, label="Theoretical target")
    ax.scatter(*mean_point, color="tab:blue", marker="+", s=120, label="Actual mean landing point")
    accuracy_dist = float(np.hypot(*accuracy_offset))
    ax.annotate("", xy=mean_point, xytext=target,
                arrowprops=dict(arrowstyle="->", color="black", lw=1.2))
    ax.set_aspect("equal")
    ax.grid(True, linestyle="--", alpha=0.4)
    ax.legend(loc="best", fontsize=8)
    ax.set_title(
        f"Accuracy = {accuracy_dist:.3f} (target -> mean offset)\n"
        f"Repeatability (std dev of scatter) = {repeatability_std:.3f}"
    )
    fig.tight_layout()
    return fig, accuracy_dist
