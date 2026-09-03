import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import streamlit as st
from core.potential_field import plan_path

st.set_page_config(page_title="Potential Field Path Planner", page_icon="🧲", layout="wide")
st.title("🧲 Potential Field Path Planner")

st.markdown(
    """
The goal acts like a magnet pulling the robot in (the pull weakens as it
gets closer, so the robot arrives with zero velocity). Each obstacle
repels the robot within its circle of influence, pushing harder the
closer the robot gets. The robot moves along the resultant of these
forces at every step.
"""
)

if "obstacles" not in st.session_state:
    st.session_state.obstacles = [(5.0, 0.3, 1.0), (5.0, 3.0, 1.0), (5.0, -3.0, 1.0)]
    st.session_state.start = (0.0, 0.0)
    st.session_state.goal = (10.0, 0.0)

col_a, col_b = st.columns(2)
if col_a.button("Load a clean example (single offset obstacle)"):
    st.session_state.start = (0.0, 0.0)
    st.session_state.goal = (10.0, 0.0)
    st.session_state.obstacles = [(5.0, 0.3, 1.0)]
if col_b.button("Load the Local Minima Problem demo (U-shaped trap)"):
    st.session_state.start = (0.0, 0.0)
    st.session_state.goal = (0.0, 20.0)
    st.session_state.obstacles = [(0.0, 6.0, 1.5), (-3.0, 3.0, 1.5), (3.0, 3.0, 1.5)]

st.subheader("Start and goal")
col1, col2, col3, col4 = st.columns(4)
start_x = col1.number_input("Start x", value=st.session_state.start[0])
start_y = col2.number_input("Start y", value=st.session_state.start[1])
goal_x = col3.number_input("Goal x", value=st.session_state.goal[0])
goal_y = col4.number_input("Goal y", value=st.session_state.goal[1])

st.subheader("Obstacles (circles)")
num_obstacles = st.number_input("Number of obstacles", min_value=0, max_value=5,
                                 value=len(st.session_state.obstacles), step=1)
obstacles = []
for i in range(int(num_obstacles)):
    default = st.session_state.obstacles[i] if i < len(st.session_state.obstacles) else (5.0, 0.0, 1.0)
    cols = st.columns(3)
    ox = cols[0].number_input(f"Obstacle {i+1} x", value=default[0], key=f"ox_{i}")
    oy = cols[1].number_input(f"Obstacle {i+1} y", value=default[1], key=f"oy_{i}")
    orad = cols[2].number_input(f"Obstacle {i+1} radius", min_value=0.1, value=default[2], key=f"or_{i}")
    obstacles.append((ox, oy, orad))

st.subheader("Field parameters")
col5, col6, col7 = st.columns(3)
k_att = col5.number_input("k_att", min_value=0.01, value=1.0)
k_rep = col6.number_input("k_rep", min_value=0.0, value=8.0)
influence_radius = col7.number_input("Influence radius", min_value=0.1, value=3.0)

obstacle_list = [((ox, oy), r) for ox, oy, r in obstacles]
path, status = plan_path((start_x, start_y), (goal_x, goal_y), obstacle_list,
                          k_att=k_att, k_rep=k_rep, influence_radius=influence_radius)
path = np.array(path)

fig, ax = plt.subplots(figsize=(7, 7))
for ox, oy, orad in obstacles:
    ax.add_patch(patches.Circle((ox, oy), orad, facecolor="tab:red", alpha=0.5))
    ax.add_patch(patches.Circle((ox, oy), orad + influence_radius, facecolor="tab:red", alpha=0.08))
ax.plot(path[:, 0], path[:, 1], color="tab:blue", linewidth=2, label="Path")
ax.scatter([start_x], [start_y], color="black", marker="o", s=80, label="Start", zorder=5)
ax.scatter([goal_x], [goal_y], color="green", marker="*", s=200, label="Goal", zorder=5)
ax.set_aspect("equal")
ax.grid(True, linestyle="--", alpha=0.4)
ax.legend(loc="best")
st.pyplot(fig)

if status == "reached":
    st.success(f"The robot reached the goal in {len(path)} steps.")
elif status == "stuck":
    st.error(
        "The robot got stuck in a local minimum -- the attractive and "
        "repulsive forces cancelled out before it reached the goal. This "
        "is the Local Minima Problem the notes describe for concave "
        "(U-shaped) obstacle arrangements."
    )
else:
    st.warning("The simulation ran out of iterations without reaching the goal or clearly getting stuck.")
