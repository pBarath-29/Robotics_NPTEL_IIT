"""Workspace geometry per coordinate system, from Lecture 5:
"Robot Workspaces & Performance Specifications".

Lecture 5 explicitly notes that 3D workspaces are hard to visualize directly,
so analysis is done via 2D cross-sections: an elevation view and a plan
(top-down) view. This module follows that same approach rather than
attempting full 3D rendering.

Reachable workspace: volume reachable with at least one orientation.
Dextrous workspace: subset reachable with multiple orientations. Computing
the exact dextrous region requires forward kinematics, which is outside the
Week 1 syllabus -- so here it is shown only as a conceptual (illustrative)
inner subset of the reachable region, consistent with the "dextrous is
always a smaller subset of reachable" rule from Lecture 4.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches


def _new_fig(title_left="Elevation view (side)", title_right="Plan view (top-down)"):
    fig, (ax_elev, ax_plan) = plt.subplots(1, 2, figsize=(9, 4.5))
    ax_elev.set_title(title_left)
    ax_plan.set_title(title_right)
    for ax in (ax_elev, ax_plan):
        ax.set_aspect("equal")
        ax.grid(True, linestyle="--", alpha=0.4)
    return fig, ax_elev, ax_plan


def cartesian_workspace(x_range, y_range, z_range):
    """Cartesian (PPP/SSS): workspace is a cuboid. Reachable == dextrous,
    since a pure-translation manipulator has only one possible orientation
    at every point (Lecture 4/5).
    """
    x_min, x_max = x_range
    y_min, y_max = y_range
    z_min, z_max = z_range

    fig, ax_elev, ax_plan = _new_fig()

    ax_elev.add_patch(patches.Rectangle(
        (x_min, z_min), x_max - x_min, z_max - z_min,
        facecolor="tab:blue", alpha=0.35, edgecolor="tab:blue", label="Reachable = Dextrous"))
    ax_elev.set_xlim(x_min - 1, x_max + 1)
    ax_elev.set_ylim(z_min - 1, z_max + 1)
    ax_elev.set_xlabel("X")
    ax_elev.set_ylabel("Z")
    ax_elev.legend(loc="upper right", fontsize=8)

    ax_plan.add_patch(patches.Rectangle(
        (x_min, y_min), x_max - x_min, y_max - y_min,
        facecolor="tab:blue", alpha=0.35, edgecolor="tab:blue"))
    ax_plan.set_xlim(x_min - 1, x_max + 1)
    ax_plan.set_ylim(y_min - 1, y_max + 1)
    ax_plan.set_xlabel("X")
    ax_plan.set_ylabel("Y")

    fig.suptitle("Cartesian workspace: cuboid")
    fig.tight_layout()
    return fig


def cylindrical_workspace(r_min, r_max, z_min, z_max):
    """Cylindrical (TSS/TPP): workspace is a cylindrical annular space.
    The twisting joint gives a full 360-degree sweep (Lecture 5).
    """
    fig, ax_elev, ax_plan = _new_fig()

    ax_elev.add_patch(patches.Rectangle(
        (r_min, z_min), r_max - r_min, z_max - z_min,
        facecolor="tab:orange", alpha=0.35, edgecolor="tab:orange", label="Reachable"))
    dex_r_min = r_min + 0.25 * (r_max - r_min)
    dex_r_max = r_max - 0.25 * (r_max - r_min)
    dex_z_min = z_min + 0.15 * (z_max - z_min)
    dex_z_max = z_max - 0.15 * (z_max - z_min)
    ax_elev.add_patch(patches.Rectangle(
        (dex_r_min, dex_z_min), dex_r_max - dex_r_min, dex_z_max - dex_z_min,
        facecolor="tab:red", alpha=0.5, edgecolor="tab:red", label="Dextrous (illustrative)"))
    ax_elev.set_xlim(0, r_max + 1)
    ax_elev.set_ylim(z_min - 1, z_max + 1)
    ax_elev.set_xlabel("Radial reach r")
    ax_elev.set_ylabel("Z")
    ax_elev.legend(loc="upper right", fontsize=8)

    ax_plan.add_patch(patches.Wedge((0, 0), r_max, 0, 360, width=r_max - r_min,
                                     facecolor="tab:orange", alpha=0.35, edgecolor="tab:orange"))
    ax_plan.set_xlim(-r_max - 1, r_max + 1)
    ax_plan.set_ylim(-r_max - 1, r_max + 1)
    ax_plan.set_xlabel("X")
    ax_plan.set_ylabel("Y")

    fig.suptitle("Cylindrical workspace: annular space, 360-degree sweep")
    fig.tight_layout()
    return fig


def spherical_workspace(r_min, r_max, elev_min_deg, elev_max_deg, twist_deg):
    """Spherical/Polar (TRS/TRP): 2D elevation reach profile swept across
    the twisting joint's rotational range (Lecture 5).
    """
    fig, ax_elev, ax_plan = _new_fig()

    ax_elev.add_patch(patches.Wedge((0, 0), r_max, elev_min_deg, elev_max_deg,
                                     width=r_max - r_min,
                                     facecolor="tab:green", alpha=0.35,
                                     edgecolor="tab:green", label="Reachable"))
    dex_span = (elev_max_deg - elev_min_deg) * 0.5
    dex_mid = (elev_max_deg + elev_min_deg) / 2
    ax_elev.add_patch(patches.Wedge((0, 0), r_max - 0.15 * (r_max - r_min),
                                     dex_mid - dex_span / 2, dex_mid + dex_span / 2,
                                     width=(r_max - r_min) * 0.6,
                                     facecolor="tab:red", alpha=0.5,
                                     edgecolor="tab:red", label="Dextrous (illustrative)"))
    lim = r_max + 1
    ax_elev.set_xlim(-lim, lim)
    ax_elev.set_ylim(-lim, lim)
    ax_elev.set_xlabel("Horizontal reach")
    ax_elev.set_ylabel("Vertical reach")
    ax_elev.legend(loc="upper right", fontsize=7)

    ax_plan.add_patch(patches.Wedge((0, 0), r_max, -twist_deg / 2, twist_deg / 2,
                                     width=r_max - r_min,
                                     facecolor="tab:green", alpha=0.35, edgecolor="tab:green"))
    ax_plan.set_xlim(-lim, lim)
    ax_plan.set_ylim(-lim, lim)
    ax_plan.set_xlabel("X")
    ax_plan.set_ylabel("Y")

    fig.suptitle(f"Spherical workspace: elevation profile swept {twist_deg} deg")
    fig.tight_layout()
    return fig


def articulated_workspace(r_min, r_max, elev_min_deg, elev_max_deg, twist_deg):
    """Revolute/Articulated (TRR): workspace formed by intersecting partial
    spheres -- the elevation cross-section is a folded/stretched region,
    swept around the base twisting joint (Lecture 5).
    """
    fig, ax_elev, ax_plan = _new_fig()

    ax_elev.add_patch(patches.Wedge((0, 0), r_max, elev_min_deg, elev_max_deg,
                                     width=r_max - r_min,
                                     facecolor="tab:purple", alpha=0.30,
                                     edgecolor="tab:purple", label="Reach band 1"))
    inner_r_max = r_max * 0.7
    ax_elev.add_patch(patches.Wedge((0, 0), inner_r_max, elev_min_deg + 20, elev_max_deg - 10,
                                     width=inner_r_max - r_min * 0.5,
                                     facecolor="tab:purple", alpha=0.30,
                                     edgecolor="tab:purple", label="Reach band 2 (folded)"))
    dex_span = (elev_max_deg - elev_min_deg) * 0.35
    dex_mid = (elev_max_deg + elev_min_deg) / 2
    ax_elev.add_patch(patches.Wedge((0, 0), r_max * 0.75,
                                     dex_mid - dex_span / 2, dex_mid + dex_span / 2,
                                     width=(r_max - r_min) * 0.4,
                                     facecolor="tab:red", alpha=0.5,
                                     edgecolor="tab:red", label="Dextrous (illustrative)"))
    lim = r_max + 1
    ax_elev.set_xlim(-lim, lim)
    ax_elev.set_ylim(-lim, lim)
    ax_elev.set_xlabel("Horizontal reach")
    ax_elev.set_ylabel("Vertical reach")
    ax_elev.legend(loc="upper right", fontsize=7)

    ax_plan.add_patch(patches.Wedge((0, 0), r_max, -twist_deg / 2, twist_deg / 2,
                                     width=r_max - r_min,
                                     facecolor="tab:purple", alpha=0.35, edgecolor="tab:purple"))
    ax_plan.set_xlim(-lim, lim)
    ax_plan.set_ylim(-lim, lim)
    ax_plan.set_xlabel("X")
    ax_plan.set_ylabel("Y")

    fig.suptitle(f"Articulated workspace: intersecting reach bands, swept {twist_deg} deg")
    fig.tight_layout()
    return fig
