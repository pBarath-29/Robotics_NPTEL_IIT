"""Applications of robotics, from Lecture 1: "Applications of Robotics"."""

DOMAINS = {
    "Manufacturing": {
        "advantages": [
            "Safety: can work in dirty and hazardous environments (e.g. nuclear power plants).",
            "Quality and productivity: higher quality, fewer errors, increased productivity.",
            "Cost efficiency: one robot can replace multiple human workers.",
            "Repetitive task endurance: no fatigue-driven mistakes or material waste.",
        ],
        "tasks": {
            "Pick and Place": "Transporting components across the machine shop before assembly.",
            "Machining": "Operating attachments for grinding, drilling, and milling complex profiles.",
            "Spray Painting": "Continuous, flawless paint application, heavily used in the automotive industry.",
            "Welding (Spot & Arc)": (
                "Robots like the PUMA perform continuous arc welding. Spot welds are placed "
                "first to lock steel plates in place before the continuous seam, to prevent "
                "distortion under heat."
            ),
        },
    },
    "Underwater": {
        "advantages": [
            "Searching for valuable gems and studying underwater environments and living creatures.",
            "Maintaining crude petroleum operations: pipeline inspection, underwater vacuum welding.",
            "Multi-legged or tracked vehicles are preferred over wheeled robots due to the rough seabed.",
        ],
        "tasks": {
            "ROV (Remotely Operated Vehicle)": "Centralized control system, operated remotely by a computer or human at the surface.",
            "AUV (Autonomous Underwater Vehicle)": "Decentralized control system, the robot is intelligent and makes its own navigational decisions.",
        },
    },
    "Medical": {
        "advantages": [
            "Allows procedures and diagnostics that would be difficult or impossible for a human alone.",
        ],
        "tasks": {
            "Telesurgery": (
                "A doctor performs surgery from a distance using a Master Robot, which "
                "controls a Slave Robot on the patient. The slave carries surgical "
                "instruments and force/torque sensors that send tactile feedback "
                "wirelessly back to the doctor."
            ),
            "Micro-Capsule Multi-Legged Robot": (
                "A swallowable, capsule-sized robot with a lithium battery and "
                "high-speed camera to detect tumors in the digestive tract. It has no "
                "motor; movement is controlled externally by the doctor using a "
                "permanent magnet."
            ),
            "Rehabilitation Robotics": "Intelligent prosthetic and orthotic devices to assist the elderly and physically impaired with walking.",
        },
    },
    "Space": {
        "advantages": [
            "Removes the need to risk human life for exploration, inspection, and maintenance tasks.",
        ],
        "tasks": {
            "Planetary Exploration": "Intelligent tracked/multi-legged rovers (Curiosity, Spirit, Opportunity) collect data on Mars.",
            "Space Stations": "Used for inspections, survey maintenance, and spacecraft deployment/retrieval.",
            "Robo-nauts & Free-Flying Robots": "Humanoid robots designed to replace astronauts, plus tiny fly-like robots in development for autonomous space data collection.",
        },
    },
    "Agriculture & Miscellaneous": {
        "advantages": [
            "Automates hazardous, repetitive, or precision-demanding duties across many industries.",
        ],
        "tasks": {
            "Agriculture": "Spraying liquid fertilizers/pesticides, cleaning weeds, sowing seeds in precise patterns, inspecting crop health.",
            "Everyday & Hazardous Duties": "Household chores, garbage collection, underground coal mining, sewage line cleaning, firefighting.",
        },
    },
}


def domain_names() -> list:
    return list(DOMAINS.keys())
