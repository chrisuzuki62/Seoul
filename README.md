# Seoul
# System Description

The goal of our project is to create a 2.5 degree of freedom pen plotter that does not operate using a cartesian coordinate system. Our system accomplishes this goal by using a four-bar linkage system that actuates similar to a SCARA robot. Any user using an HPGL file to replicate their digital drawing will be able to use this device.


# Hardware Design

Our system consists of a robot arm-type system inspired by the Line-us drawing robot. We will use the two Pittman DC geared motors found in the ME405 tubs to control a set of four linkages. The two motors will me mounted inline vertically, facing each other, and connect at the center location to two of the linkages. A Tower Pro SG90 servo motor borrowed from the robotics lab will be used to control an up and down movement to raise and lower the pen from the drawing surface. We will have a 2.5 degree of freedom system with two degrees of freedom from the two DC geared motors and a half degree of freedom from the servo motor to raise and lower the system. The four linkages form a semi-diamond shape that creates a robot arm that functions similarly to a SCARA-type robot arm. We plan on 3D printing the linkages from PLA plastic. The motors will be mounted on a 3D-printed frame. Additional components required for the up and down movement of the system will also be 3D-printed. Gears and bearings will be added to improve the resolution and smoothness of our robot's movements. The current design of the Drawing bot is seen in Figure 1. below.


![test](system.png)

Figure 1. CAD of concept Drawing Bot

# Software Design

The program for our plotter reads from an HPGL file uploaded onto the Nucleo micrcoprocessor and carries out each step of the file to create a 2D drawing. The X-Y coordinates specified in the HPGL file are sequentially inputted into a function that calculates the inverse kinematics for both of the driven linkages on our robot. The program also allows for the location and size of the drawing to be altered as long as the drawing area is within the robot's reach. For more information on the layout our asynchronous cooperative multitasking program, please refer to our Documentation of Code linked below.

Documentation of Code: https://chrisuzuki62.github.io/me405_termproject/

# Results

The final demonstration video can be seen here: https://youtu.be/_0DGsNZlUL0



# Resources
Reference for hand tracking: https://google.github.io/mediapipe/solutions/hands.html
