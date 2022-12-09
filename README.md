# Seoul
# System Description

The purpose of this project is to create a hand gesture recognition library that is able to conduct a task once a hand gesture is recognized. The goal is to apply this to automobiles, where a driver’s hand gesture will trigger the activation/modification of a car feature (ex. turning on/off the wipers, changing the music track, etc.).


# Hardware Design

Requirements:
1. Preferable - Intel Realsense L515 Camera
    a. USB 3.0 Connection
3. ELP Camera - https://www.amazon.com/ELP-Fisheye-170degree-Infrared-Housing/dp/B07DWWSWNH/ref=sr_1_1_sspa?keywords=elp+camera&qid=1670627370&sr=8-1-spons&ufe=app_do%3Aamzn1.fos.18ed3cb5-28d5-4975-8bc7-93deae8f9840&psc=1&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUFZWUVNQTdLR0pRSFEmZW5jcnlwdGVkSWQ9QTA5NTY1OTBRSzhQSVUwNU1OSlomZW5jcnlwdGVkQWRJZD1BMDk5MjM2MzNIR0paR0dUNFpKWkgmd2lkZ2V0TmFtZT1zcF9hdGYmYWN0aW9uPWNsaWNrUmVkaXJlY3QmZG9Ob3RMb2dDbGljaz10cnVl


# Software Design

The program for our plotter reads from an HPGL file uploaded onto the Nucleo micrcoprocessor and carries out each step of the file to create a 2D drawing. The X-Y coordinates specified in the HPGL file are sequentially inputted into a function that calculates the inverse kinematics for both of the driven linkages on our robot. The program also allows for the location and size of the drawing to be altered as long as the drawing area is within the robot's reach. For more information on the layout our asynchronous cooperative multitasking program, please refer to our Documentation of Code linked below.

![test](system.png)

Figure 1. Flow Logic of the Code

# Results

The final demonstration video can be seen here: https://youtu.be/_0DGsNZlUL0



# Resources
Reference for hand tracking: https://google.github.io/mediapipe/solutions/hands.html
