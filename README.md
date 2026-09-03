# Robotics IIT

This repository holds my notes and personal projects for the NPTEL course Robotics.

## How this repository is organized

There are two main folders here.

**Notes** holds my personal notes from each week of the course.

**Projects** holds small projects that I build after finishing each week. I do this so I actually use what I learned instead of just leaving it as notes. Each project has its own folder named after the week it is based on.

## Projects

### Week 1 Project

Week 1 covers the introduction to robots and robotics, the components that make up a robotic system, joint types and degrees of freedom, Grubler's Criterion for calculating manipulator mobility, how robots are classified, and how their workspace is analyzed.

After finishing this week, I built a small Streamlit app to actually use these ideas instead of just reading them. It lets you look up a joint type and see its degrees of freedom, calculate a manipulator's mobility with Grubler's Criterion, figure out what kind of manipulator a robot is from its joint sequence, see what shape its workspace would take, and calculate basic performance specs like resolution and repeatability.

Access it at : https://roboticsnpteliit-ssufpw6oeu2r2z3edrf7gt.streamlit.app/

### Week 2 Project

Week 2 covers applications of robotics across manufacturing, underwater, medical, space, and agriculture, end-effectors and grippers, robot teaching methods and the VAL programming language, economic analysis of a robot purchase, and the basics of frame transformations.

For this week I built another Streamlit app to put these ideas into practice. It lets you browse robotics applications by domain, look up gripper types and designs, calculate the lift force of a vacuum gripper, build a VAL pick-and-place program, work out whether a robot purchase pays off financially, and compose translation and rotation operators into a single transformation and apply it to a point.

Access it at : https://roboticsnpteliit-bqxwnnlegzdrfkpfbbhhfp.streamlit.app/

### Week 3 Project

Week 3 is where the actual kinematics starts: rotation matrices and their properties, the composite rotation rule, cylindrical and spherical coordinate mapping, Roll-Pitch-Yaw and Euler angle orientation, Denavit-Hartenberg notation, and forward and inverse kinematics.

For this week I built another Streamlit app to work through these ideas. It lets you check whether a matrix is a valid rotation matrix, convert cylindrical or spherical coordinates to Cartesian, build or extract Roll-Pitch-Yaw and Euler angle orientations, build a Denavit-Hartenberg table and compute forward kinematics, and solve the inverse kinematics of a 2-DoF planar arm.

Access it at : https://roboticsnpteliit-hzegrrhuzmjifxxanbxjhz.streamlit.app/

### Week 4 Project

Week 4 covers the forward and inverse kinematics of a 5-DoF manipulator (the MINIMOVER), two more Denavit-Hartenberg examples, trajectory planning, and Jacobians and singularities.

For this week I built another Streamlit app to work through these ideas. It lets you compute the MINIMOVER's end-effector pose from its joint angles, solve for the joint angles that reach a target pose, browse two more worked DH parameter assignments, fit cubic, quintic, or parabolic-blend trajectories, and check a 2-DoF arm pose for singularities.

Access it at : https://roboticsnpteliit-gpfyjmpax4zslhbvasbrz2.streamlit.app/

### Week 5 Project

Week 5 is where kinematics gives way to dynamics: inertia tensors for robot links, the Lagrange-Euler formulation, the D/h/C term structure of joint torque, and a more tractable Center of Mass method for deriving the torque equations of a 2-DoF arm by hand.

For this week I built another Streamlit app to work through these ideas. It lets you compute a link's inertia tensor and its center-of-mass value, browse the dynamics concepts and torque term structure, see why the trace of V*V^T gives kinetic energy, and calculate the joint torques needed to move a 2-link arm, with built-in consistency checks on the result.

Access it at : https://roboticsnpteliit-p4behseayymudddqtukcjw.streamlit.app/

### Week 6 Project

Week 6 covers how a robot actually senses and controls itself: partitioned control and PD/PID joint control laws, sensor classification and position/force/range sensors, and the beginnings of robot vision.

For this week I built another Streamlit app to work through these ideas. It lets you tune a PD/PID joint controller and watch it track a target angle, browse how sensors are classified, compute absolute encoder resolution and incremental encoder direction, use voltage-divider and wrist force/moment sensor calculators, compute triangulation range sensor distance, and apply a 3x3 convolution mask to a small image grid.

Access it at : https://roboticsnpteliit-pl5ohd4fqezkqwmo9ed3e7.streamlit.app/

### Week 7 Project

Week 7 finishes robot vision (neighborhood averaging and median filtering, thresholding, edge detection, boundary descriptors) and then introduces robot motion planning: graph-based algorithms, dynamic planning, and the Potential Field Method.

For this week I built another Streamlit app to work through these ideas. It lets you apply averaging and median filters to a small image grid, threshold and edge-detect an image with gradient/Laplacian masks, compute chain codes, signatures, and compactness for shape identification, browse a reference of the motion planning algorithms, and simulate a robot navigating to a goal around obstacles with the Potential Field Method, including the Local Minima Problem.

The project is in Projects/Week_7_Project. To run it, install the requirements with pip and then run app.py with streamlit.
