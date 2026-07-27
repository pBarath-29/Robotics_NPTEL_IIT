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

The project is in Projects/Week_1_Project. To run it, install the requirements with pip and then run app.py with streamlit.

### Week 2 Project

Week 2 covers applications of robotics across manufacturing, underwater, medical, space, and agriculture, end-effectors and grippers, robot teaching methods and the VAL programming language, economic analysis of a robot purchase, and the basics of frame transformations.

For this week I built another Streamlit app to put these ideas into practice. It lets you browse robotics applications by domain, look up gripper types and designs, calculate the lift force of a vacuum gripper, build a VAL pick-and-place program, work out whether a robot purchase pays off financially, and compose translation and rotation operators into a single transformation and apply it to a point.

The project is in Projects/Week_2_Project. It is run the same way as the Week 1 project.
