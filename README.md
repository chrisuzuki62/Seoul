# Team Seoul
Group members: Rithwik JayanthSteven Shang ShiChris SuzukiLeo Chen

# System Description

The purpose of this project is to create a hand gesture recognition library that is able to conduct a task once a hand gesture is recognized. The goal is to apply this to automobiles, where a driver’s hand gesture will trigger the activation/modification of a car feature (ex. turning on/off the wipers, changing the music track, etc.).


# Hardware Design
The Design uses the Intel Realsense L515 for RGB, IR, and Depth Camera capabilties.
Requirements:
1. Preferable - Intel Realsense L515 Camera
    a. USB 3.0 Connection
3. ELP Camera - https://www.amazon.com/ELP-Fisheye-170degree-Infrared-Housing/dp/B07DWWSWNH/ref=sr_1_1_sspa?keywords=elp+camera&qid=1670627370&sr=8-1-spons&ufe=app_do%3Aamzn1.fos.18ed3cb5-28d5-4975-8bc7-93deae8f9840&psc=1&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUFZWUVNQTdLR0pRSFEmZW5jcnlwdGVkSWQ9QTA5NTY1OTBRSzhQSVUwNU1OSlomZW5jcnlwdGVkQWRJZD1BMDk5MjM2MzNIR0paR0dUNFpKWkgmd2lkZ2V0TmFtZT1zcF9hdGYmYWN0aW9uPWNsaWNrUmVkaXJlY3QmZG9Ob3RMb2dDbGljaz10cnVl


# Software Design

We use a MediaPipe and Tensor Flow package referred in the resource section to track hands and their finger positions like image below:

![test1](mediapipe.png)


Figure 1. Hands Package Results

Using the data from the fingertip positions we 
Implemented Features
Volume/Temp Change
Next/Previous Track
Answer Incoming Calls
etc



![test](system.png)

Figure 2. Flow Logic of the Code

# Results

The final demonstration video of each function can be seen here: https://github.com/chrisuzuki62/Seoul/tree/main/video_demo


# Resources
Reference for hand tracking: https://google.github.io/mediapipe/solutions/hands.html
