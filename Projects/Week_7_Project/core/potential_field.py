"""The Potential Field Method for motion planning, from Lecture 5 (Khatib, 1986).

Attractive potential: a parabolic well centered on the goal, so the pull
toward the goal decreases with distance and reaches zero exactly at the
goal (matching the notes: "the robot slows down and stops with zero
velocity exactly at the goal").
    F_att(q) = k_att * (goal - q)

Repulsive potential: zero outside an obstacle's circle of influence
(radius rho0); inside it, the push grows without bound as the robot
approaches the obstacle boundary (matching "exponentially stronger the
closer the robot gets").
    F_rep(q) = k_rep * (1/rho - 1/rho0) * (1/rho^2) * unit_vector_away_from_obstacle
    where rho = distance from q to the obstacle's boundary.

The resultant force is the vector sum of the attractive force and every
obstacle's repulsive force. A path is planned by repeatedly stepping in
the direction of the resultant force (gradient descent on the potential).
"""

import numpy as np


def attractive_force(q, goal, k_att: float) -> np.ndarray:
    q, goal = np.asarray(q, dtype=float), np.asarray(goal, dtype=float)
    return k_att * (goal - q)


def repulsive_force(q, obstacle_center, obstacle_radius: float, influence_radius: float, k_rep: float) -> np.ndarray:
    q = np.asarray(q, dtype=float)
    center = np.asarray(obstacle_center, dtype=float)
    diff = q - center
    dist_to_center = np.linalg.norm(diff)
    rho = dist_to_center - obstacle_radius

    if rho <= 0:
        rho = 1e-6  # avoid dividing by zero if the robot is touching/inside the obstacle
    if rho > influence_radius:
        return np.zeros(2)

    direction = diff / dist_to_center if dist_to_center > 1e-9 else np.array([1.0, 0.0])
    magnitude = k_rep * (1.0 / rho - 1.0 / influence_radius) * (1.0 / rho ** 2)
    return magnitude * direction


def total_force(q, goal, obstacles: list, k_att: float, k_rep: float, influence_radius: float) -> np.ndarray:
    force = attractive_force(q, goal, k_att)
    for center, radius in obstacles:
        force = force + repulsive_force(q, center, radius, influence_radius, k_rep)
    return force


def plan_path(start, goal, obstacles: list, k_att: float = 1.0, k_rep: float = 1.0,
              influence_radius: float = 2.0, step_eta: float = 0.05,
              max_step: float = 0.2, max_iters: int = 2000, goal_tolerance: float = 0.1,
              stuck_window: int = 30, stuck_tolerance: float = 0.05):
    """Steps the robot along the resultant force field from start to goal,
    q_new = q + eta * F (capped at max_step), so the step naturally shrinks
    as the robot nears an equilibrium instead of oscillating around it at
    a fixed amplitude.

    Returns (path, status) where status is "reached", "stuck" (a local
    minimum -- the robot has made negligible net progress over the last
    stuck_window steps without reaching the goal), or "max_iters".
    """
    q = np.asarray(start, dtype=float)
    goal = np.asarray(goal, dtype=float)
    path = [q.copy()]

    for _ in range(max_iters):
        if np.linalg.norm(goal - q) < goal_tolerance:
            return path, "reached"

        force = total_force(q, goal, obstacles, k_att, k_rep, influence_radius)
        step = step_eta * force
        step_mag = np.linalg.norm(step)
        if step_mag > max_step:
            step = step * (max_step / step_mag)

        q = q + step
        path.append(q.copy())

        if len(path) > stuck_window:
            net_progress = np.linalg.norm(path[-1] - path[-1 - stuck_window])
            if net_progress < stuck_tolerance:
                return path, "stuck"

    return path, "max_iters"
