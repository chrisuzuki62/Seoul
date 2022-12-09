from helper_functions import *
import cv2
import numpy as np
import mediapipe as mp
import math

def volume_control(hands, mpHands, mpDraw, cap):
    # while True:
    volbar = 0
    volper = 0
    success, img = cap.read() #If camera works capture an image
    imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB) #Converts image to rgb
    
    #Collection of gesture information
    results = hands.process(imgRGB) #completes the image processing.

    lmList = [] #empty list
    if results.multi_hand_landmarks: #list of all hands detected.
        #By accessing the list, we can get the information of each hand's corresponding flag bit
        for handlandmark in results.multi_hand_landmarks:
            for id,lm in enumerate(handlandmark.landmark): #adding counter and returning it
                # Get finger joint points
                h,w,_ = img.shape #gets height and width of image
                cx,cy = int(lm.x*w),int(lm.y*h)
                lmList.append([id,cx,cy]) #adding to the empty list 'lmList'
            mpDraw.draw_landmarks(img,handlandmark,mpHands.HAND_CONNECTIONS)
    
        if lmList != []:
            #getting the value at a point
                    #x position  #y position
            x1,y1 = lmList[4][1],lmList[4][2]  #thumb
            x2,y2 = lmList[8][1],lmList[8][2]  #index finger
            x3,y3 = lmList[12][1], lmList[12][2]
            x4,y4 = lmList[16][1], lmList[16][2]
            x5,y5 = lmList[20][1], lmList[20][2]

            x2b, y2b = lmList[5][1],lmList[5][2]
            x3b, y3b = lmList[9][1],lmList[9][2]
            x4b, y4b = lmList[13][1],lmList[13][2]
            x5b, y5b = lmList[17][1],lmList[17][2]

            # 4 - thumb
            # 8 - index finger
            # 12 - middle finger
            # 16 - ring finger
            # 20 - litte finger

            # #creating circle at the tips of thumb and index finger
            # cv2.circle(img,(x1,y1),13,(255,0,0),cv2.FILLED) #image #fingers #radius in rgb
            # cv2.circle(img,(x2,y2),13,(255,0,0),cv2.FILLED) #image #fingers #radius in rgb  
            # cv2.circle(img,(x3,y3),13,(255,0,0),cv2.FILLED)
            # cv2.circle(img,(x4,y4),13,(255,0,0),cv2.FILLED)
            # cv2.circle(img,(x4,y4),13,(255,0,0),cv2.FILLED)


            # cv2.line(img,(x1,y1),(x2,y2),(255,0,0),3)
            # cv2.line(img,(x2,y2),(x3,y3),(255,0,0),3)
            # cv2.line(img,(x3,y3),(x4,y4),(255,0,0),3)
            # cv2.line(img,(x4,y4),(x5,y5),(255,0,0),3)  

            length2 = math.hypot(x2-x2b,y2-y2b)
            length3 = math.hypot(x3-x3b,y3-y3b)
            length4 = math.hypot(x4-x4b,y4-y4b)
            length5 = math.hypot(x5-x5b,y5-y5b)
            lengtht = math.hypot(x1-x5b,y1-y5b)
            # length_23 = math.hypot(x2-x3,y2-y3)

            if length3 < 80 and length4 < 80 and length5 < 80 and length2 > 80 and lengtht >80: # and length_23 > 50:

                length = math.hypot(x2-x1,y2-y1) #distance b/w tips using hypotenuse
                # using numpy we find our length by converting hand range in terms of volume range ie between -63.5 to 0

                volbar=np.interp(length,[30,350],[400,150])
                volper=np.interp(length,[30,350],[0,100])

            
                return volbar, volper
            
            else:
                volbar = 0
                return volbar, volper
    
    else:
        volbar = 0
        volper = 0
        return volbar, volper





