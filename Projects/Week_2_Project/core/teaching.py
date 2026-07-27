"""Robot teaching methods and VAL programming, from Lecture 3-4."""

ONLINE_METHODS = {
    "Control Handle / Joystick": "Physically steering the robot arm to a point and storing the joint angles via optical encoders.",
    "Push Buttons": "Using the controller panel to jog the robot in Cartesian or joint space.",
    "Teach-Pendant": "A remote control device used to manually drive the robot to desired points and save them.",
    "Lead-Through (Continuous Path)": (
        "For tasks where the tool must stay in continuous contact with the job. A "
        "lightweight 'Robot Simulator' (a kinematically identical dummy arm with "
        "optical encoders but no motors/brakes) is manually traced by the operator; "
        "the encoders record thousands of continuous points to feed to the main robot."
    ),
}

OFFLINE_METHODS = {
    "VAL (Variable/Versatile Assembly Language)": (
        "A language specific to the PUMA series robots (Programmable Universal "
        "Machine for Assembly), using BASIC-like commands. Programming is done "
        "without using the physical robot."
    ),
}

# Ordered pick-and-place command template from Lecture 4, with the exact
# syntax and purpose of each step.
VAL_PICK_AND_PLACE_TEMPLATE = [
    ("APPRO {part}, {approach_mm}", "Approach the part, stopping {approach_mm}mm above it (Z-direction)."),
    ("MOVES {part}", "Move in a straight line directly to the part."),
    ("CLOSEI", "Close the gripper to grasp the object, followed by a short delay."),
    ("DEPARTS {depart1_mm}", "Depart in a straight line by {depart1_mm}mm (Z-direction)."),
    ("APPROS {bin}, {bin_approach_mm}", "Approach in a straight line to a point {bin_approach_mm}mm above the target bin."),
    ("MOVE {bin}", "Move directly to the target bin."),
    ("OPENI", "Open the gripper to release the object, followed by a short delay."),
    ("DEPART {depart2_mm}", "Depart upwards by {depart2_mm}mm (Z-direction)."),
]

VAL_OTHER_COMMANDS = {
    "SPEED 40": "Sets the robot's movement speed to 40% of its maximum rated motor speed.",
    "EXECUTE / ABORT": "Run or stop the current program.",
    "EDIT [filename]": "Opens a saved program for modification.",
    "STORE / LOAD [filename]": "Saves or loads a program to/from memory.",
    "LISTF / DELETE": "Lists all files in the directory, or deletes a specific file/line.",
}


def build_pick_and_place(part="PART", bin_name="BIN", approach_mm=100, depart1_mm=200,
                          bin_approach_mm=300, depart2_mm=100) -> str:
    """Fill the VAL pick-and-place template with the given values."""
    lines = []
    for cmd, _ in VAL_PICK_AND_PLACE_TEMPLATE:
        lines.append(cmd.format(
            part=part, bin=bin_name, approach_mm=approach_mm,
            depart1_mm=depart1_mm, bin_approach_mm=bin_approach_mm, depart2_mm=depart2_mm,
        ))
    return "\n".join(lines)
