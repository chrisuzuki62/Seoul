from helper_functions import *
import cv2
import numpy as np
import mediapipe as mp
import math as hypot

def volume_control(mode, fing_list):           

    x1, y1 = fing_list[0], fing_list[1] #thumb
    x2, y2, = fing_list[2], fing_list[3] #index
    x3, y3, = fing_list[4], fing_list[5] #middle
    x4, y4, = fing_list[6], fing_list[7] #ring
    x5, y5, = fing_list[8], fing_list[9] #pinky

     #creating circle at the tips of thumb and index finger
    cv2.circle(img,(x1,y1),13,(255,0,0),cv2.FILLED) #image #fingers #radius in rgb
    cv2.circle(img,(x2,y2),13,(255,0,0),cv2.FILLED) #image #fingers #radius in rgb  
    cv2.circle(img,(x3,y3),13,(255,0,0),cv2.FILLED)
    cv2.circle(img,(x4,y4),13,(255,0,0),cv2.FILLED)
    cv2.circle(img,(x4,y4),13,(255,0,0),cv2.FILLED)

    cv2.line(img,(x1,y1),(x2,y2),(255,0,0),3)
    cv2.line(img,(x2,y2),(x3,y3),(255,0,0),3)
    cv2.line(img,(x3,y3),(x4,y4),(255,0,0),3)
    cv2.line(img,(x4,y4),(x5,y5),(255,0,0),3)  #create a line between tips of index finger and thumb. This will determine the current volume

    length = hypot(x2-x1,y2-y1) #distance b/w tips using hypotenuse
    # using numpy we find our length by converting hand range in terms of volume range ie between -63.5 to 0

    volbar=np.interp(length,[30,350],[400,150])
    volper=np.interp(length,[30,350],[0,100])
    
    # Hand range 30 - 350
    # Volume range -63.5 - 0.0
    #creating volume bar for volume level 
    cv2.rectangle(img,(50,150),(85,400),(0,0,255),4) # vid ,initial position ,ending position ,rgb ,thickness
    cv2.rectangle(img,(50,int(volbar)),(85,400),(0,0,255),cv2.FILLED)
    cv2.putText(img,f"{int(volper)}%",(10,40),cv2.FONT_ITALIC,1,(0, 255, 98),3)





    if mode == 0: #base mode - volume
        img = cv2.putText(img, 'Volume control', (80,80), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 0, 0))
    elif  mode == 1: #base mode - volume
        img = cv2.putText(img, 'Termperature control', (80,80), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 0, 0))
