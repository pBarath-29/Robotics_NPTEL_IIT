"""End-effector and gripper classification, from Lectures 2-3."""

CLASSIFICATION_AXES = {
    "Single vs. Double": {
        "Single Gripper": "One independent grasping unit.",
        "Double Gripper": "Two independent grasping mechanisms attached to the wrist.",
    },
    "Internal vs. External": {
        "Internal Gripper": "Grips an object (like a hollow pipe) by pressing its pads outward from the inside.",
        "External Gripper": "Grips an object by clamping down on the outside surface.",
    },
    "Soft vs. Hard": {
        "Hard Gripper": (
            "Point contact, relies on Force Closure -- strict pressure to prevent "
            "slipping, like gripping a perfectly round chalk."
        ),
        "Soft Gripper": (
            "Area contact, often relies on Form Closure -- the object's own geometry "
            "(e.g. the corners of a square chalk) helps secure the grip with less "
            "applied force."
        ),
    },
    "Active vs. Passive": {
        "Active Gripper": "Equipped with sensors (like touch sensors in human skin) to give feedback during grasping.",
        "Passive Gripper": "A purely mechanical gripper without any sensory feedback.",
    },
}

MECHANICAL_DESIGNS = {
    "Linkage Actuation": "A sliding piston connects to linkages that alter the joint angle to pinch or release the jaws.",
    "Swing-Block Mechanism": "A piston drives a link through circular grooves in two swing-blocks; as the piston slides forward, the blocks are forced together.",
    "Rack and Pinion Mechanism": "A rotating pinion drives two opposed racks connected to the gripper pads. Clockwise rotation closes the grip, counter-clockwise opens it.",
    "Cam and Follower Mechanism": "The piston drives a cam profile against roller followers, forcing them apart (open) or together (close).",
}

SPECIALIZED_GRIPPERS = {
    "Magnetic Gripper": {
        "description": "For magnetic materials only (e.g. steel, not stainless steel). Permanent magnet or electromagnet.",
        "drawback": "Subject to residual magnetism.",
        "ungripping": "Permanent magnet: needs a mechanical stripping device (e.g. a steel pin) to weaken the field. Electromagnet: simply reverse the polarity.",
    },
    "Adhesive Gripper": {
        "description": "Suitable only for very light objects, similar to a frog catching an insect with a sticky substance.",
        "drawback": "Limited to light loads.",
        "ungripping": "Not applicable in the same way -- adhesive grippers are used for light, temporary holds.",
    },
    "Universal Gripper": {
        "description": "Highly sophisticated, robust, and flexible, mimicking the human hand to grip objects of multiple shapes and sizes.",
        "drawback": "Complex and expensive relative to simple mechanical grippers.",
        "ungripping": "Depends on the specific mechanism; generally controlled release across multiple contact points.",
    },
}

RCC_PEG_IN_HOLE = {
    "lateral_error": "The peg is slightly misaligned with the hole and collides with the surface.",
    "angular_error": "Occurs if chamfering is added to fix lateral error, causing the peg to tilt and jam.",
    "solution": (
        "RCC (Remote Center Compliance): a passive gripper structure using flexible "
        "links that lets the peg naturally oscillate and guide itself into the hole "
        "through trial and error. Requires hole chamfering of less than 45 degrees, "
        "and only works vertically."
    ),
}
