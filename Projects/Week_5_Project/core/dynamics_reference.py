"""Reference data for dynamics concepts, from Lectures 1 and 3-5."""

DYNAMICS_TYPES = {
    "Inverse Dynamics": (
        "Calculates the required joint torques/forces (outputs) from known "
        "joint positions, velocities, and accelerations (inputs). This is "
        "the standard robotic control calculation."
    ),
    "Forward Dynamics": (
        "Calculates the resulting joint positions/velocities/accelerations "
        "(outputs) given specific applied torques/forces (inputs). This "
        "requires complex modeling tools like neural networks or fuzzy logic."
    ),
}

TORQUE_COMPONENTS = {
    "Inertia Terms": "Based on the mass distribution of the link.",
    "Centrifugal Force": "Outward force due to rotation.",
    "Coriolis Force": "Occurs specifically when a sliding joint moves along a rotating link.",
    "Gravity Terms": "The force required to hold the link against gravity.",
    "Friction Terms": "Mechanical resistance in the joint.",
}

DH_TERM_STRUCTURE = {
    "D_ic (Inertia term)": "D_ic = sum over j from max(i,c) to n of Trace(U_jc * J_j * U_ji^T)",
    "h_icd (Coriolis/Centrifugal term)": "h_icd = sum over j from max(i,c,d) to n of Trace(U_jcd * J_j * U_ji^T)",
    "C_i (Gravity term)": "C_i = sum over j from i to n of [-m_j * g_bar * U_ji * r_j^j]",
}

NOTABLE_FACTS_2DOF = [
    "D_12 always equals D_21 (the inertia coupling matrix is symmetric).",
    "For this specific 2-DoF arm, h_212 = h_221 = h_222 = 0.",
    "The gravity vector is padded with a zero to become a 1x4 row so it can multiply the 4x1 position vector: [gx, gy, gz, 0].",
]
