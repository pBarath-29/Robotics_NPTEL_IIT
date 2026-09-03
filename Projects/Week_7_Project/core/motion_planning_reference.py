"""Motion planning concepts and algorithm reference, from Lectures 3-4 and 6."""

MOTION_PLANNING_TYPES = {
    "Gross Motion Planning (Free Space Planning)": "Finding a feasible, collision-free path through an environment.",
    "Fine Motion Planning (Compliant Motion Planning)": "Managing physical contact and force application (e.g. how much force to apply writing on a chalkboard without breaking the marker).",
}

PROBLEM_TYPES = {
    "Manipulation Problem": "Moving a robotic arm (serial or parallel manipulator) through a workspace to reach a specific point.",
    "Navigation Problem": "Moving a mobile robot (wheeled, legged, or tracked) through an environment from start to finish.",
}

ENVIRONMENT_TYPES = {
    "Structured Environment (Find-Path Problem)": "The complete layout is known beforehand, all obstacles are static. Allows Global/Offline planning (act-after-thinking).",
    "Unstructured Environment (Dynamic Motion Planning)": "Contains moving or unknown elements. Requires Local/Online planning (act-while-thinking), constantly updating the path.",
}

GRAPH_BASED_ALGORITHMS = {
    "Visibility Graph": {
        "proposer": "Nilsson, 1969",
        "summary": (
            "The robot is a point; obstacles are static 2D polygons. Draw "
            "straight lines from the start to every visible obstacle "
            "vertex, then between visible vertices, until reaching the "
            "goal. Generates all collision-free paths; a separate search "
            "is needed to find the shortest one."
        ),
    },
    "Voronoi Diagram": {
        "proposer": "Dunlaing et al., 1986",
        "summary": (
            "Connects the midpoints (equidistant points) between "
            "obstacle and workspace boundaries into a locus, maximizing "
            "clearance from hazards. Very safe, but not time-optimal."
        ),
    },
    "Cell Decomposition (Configuration Space)": {
        "proposer": "Lozano Perez, 1983",
        "summary": (
            "Shrinks the robot to a point and grows the obstacles by the "
            "same amount (Configuration Space), then divides the "
            "remaining feasible zone into cells the robot hops between "
            "via their center points."
        ),
    },
    "Tangent Graph": {
        "proposer": "Liu and Arimoto, 1991",
        "summary": (
            "Bounds each obstacle with a circle and connects them with "
            "tangent lines and arcs. Produces short, near-optimal paths, "
            "but is O(N^2) in the number of obstacles."
        ),
    },
}

DYNAMIC_PLANNING_METHODS = {
    "Path Velocity Decomposition": {
        "proposer": "Kant and Zucker, 1984",
        "summary": "Splits into a static Path Planning Problem and a Velocity Planning Problem. Locking the path in means it must rely on jerky velocity changes, and fails with too many moving obstacles.",
    },
    "Accessibility Graphs": {
        "proposer": "Fujimura and Samet, 1988",
        "summary": "Adds a time dimension to the Visibility Graph, building a new graph per time step. Too computationally expensive for real-time use.",
    },
    "Incremental Planning": {
        "proposer": "Slack and Miller, 1987",
        "summary": "Follows a static path until obstacles invalidate it, then stops and replans. Constant stopping makes it inefficient.",
    },
    "Relative Velocity Scheme": {
        "proposer": "(various)",
        "summary": "Calculates the robot's velocity relative to each moving obstacle, converting the dynamic problem into simpler static ones.",
    },
    "Potential Field Method": {
        "proposer": "Khatib, 1986",
        "summary": "The most popular traditional algorithm: an attractive field pulls the robot toward the goal, a repulsive field pushes it away from obstacles within a circle of influence. Suffers from the Local Minima Problem in U-shaped obstacles.",
    },
}

COMPLEXITY_CLASSES = {
    "NP-Hard": "Canny and Reif (1987): motion planning for a point robot among dynamic obstacles in a 2D plane with bounded velocity.",
    "PSPACE-Hard": "Reif and Sharir (1985): the same problem expanded into 3D space.",
}

REACTIVE_CONTROL = {
    "proposer": "Brooks, 1986",
    "summary": (
        "Behaviour-based robotics: breaks a complex action into a "
        "hierarchy of simple, independent primitive behaviors (e.g. "
        "'find ball', 'avoid obstacle', 'kick'), each controlled by its "
        "own layer overseen by a supervisory computer."
    ),
    "drawbacks": [
        "Complex tasks need many behavioral layers, becoming bloated and memory-intensive.",
        "Cannot adapt to scenarios the programmer did not explicitly foresee and program a behavior for.",
    ],
}

EVOLUTIONARY_ROBOTICS = {
    "Evolution": "Optimizes the system slowly over many generations, mimicked with Genetic Algorithms or Particle Swarm Optimization.",
    "Learning": "Adapts within a single lifetime to immediate scenarios, mimicked with Neural Networks or Fuzzy Logic.",
}
