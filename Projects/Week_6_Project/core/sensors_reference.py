"""Sensor classification and characteristics, from Lecture 2."""

LOCATION_CLASSES = {
    "Internal Sensors": (
        "Used to operate and monitor the robot's internal drive units "
        "(e.g. position, velocity, acceleration, and joint force/moment "
        "sensors). Similar to a human feeling muscle pain."
    ),
    "External Sensors": (
        "Used to collect information about the outside environment (e.g. "
        "proximity, acoustic, visual, and temperature sensors). Similar to "
        "human eyes and ears."
    ),
}

CONTACT_CLASSES = {
    "Contact - Touch/Tactile (Binary)": "Indicates only whether contact has been made (1s and 0s). Does not measure force. Examples: micro-switches, limit switches, float valves.",
    "Contact - Force (Analog)": "Measures the actual magnitude of force or torque applied, typically using strain gauges.",
    "Non-Contact": "Measures properties without physical contact (e.g. range, visual, acoustic, and proximity sensors).",
}

CHARACTERISTICS = {
    "Range": "The minimum and maximum values the sensor can measure.",
    "Response": "How quickly the sensor reacts to a change in the physical variable.",
    "Accuracy": "The maximum deviation between the measured value and the exact/true quantity.",
    "Sensitivity": "The ratio of the change in output to the change in input. Constant sensitivity means the sensor is 'linear'.",
    "Repeatability": "The consistency of the readings when measuring the exact same quantity multiple times.",
    "Resolution": "The 'least count', or the smallest detectable change the sensor can register.",
}
