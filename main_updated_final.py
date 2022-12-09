# import libraries
import cv2 as cv
import numpy as np
import mediapipe as mp
import uuid
import os
from datetime import datetime, timedelta
import datacollect


# import self-defined funcs
from main_functions import *
from helper_functions import *

collect_data = datacollect.data()

# set up mediapipe and camera
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
mp_hands_hands = mp_hands.Hands()

cap = cv.VideoCapture(0)

# initialize helper vars

# change_track
isThumbRightFirst = False
isThumbLeftFirst = False
prev_thumbTip_x_next = -1
prev_thumbTip_x_prev = -1
text_print_end_time = datetime.now() - timedelta(days = 10)
text_to_print = ''
text_to_print_2 = ''
count = 0

# handle_calls
isHandStraightFlatFirst = False
call_awaiting_response = False
prev_x_mean = -1
isRejectCall = False
isPickUpCall = False
changeflag = False

# mode
mode = 0 #DUMMY
flag1 = False
flag2 = False
size_list = 10
mode_endtime = datetime.now()

volbar = 0
volper = 0
i = 0
flagp = True

all_printable_texts = ['Next Track', 'Previous Track', 'Increase Temp', 'Decrease Temp']

modes_dict = {2:'Phone Call', 0:'Media', 1:'Climate'}

with mp_hands.Hands(min_detection_confidence = 0.8, min_tracking_confidence = 0.5) as hands:
    while cap.isOpened():

        # read camera feed
        ret, frame = cap.read()

        # cvt to img
        image = cv.cvtColor(frame, cv.COLOR_BGR2RGB)

         # flip on vertical axis, so left&right hand is on left&right side   
        image = cv.flip(image, 1)

        # set flags
        image.flags.writeable = False

        # write to img
        results = hands.process(image)
        image.flags.writeable = True
        image = cv.cvtColor(image, cv.COLOR_RGB2BGR)


        ## Simulating getting a call by pressing letter c
        if cv.waitKey(33) == ord('c'):
            print('Getting a call')
            mode = 2
            flag2 = True
            start_time = datetime.now()
            text_to_print =  'Incoming Call from'
            text_to_print_2 = 'Kenji Shimada'
            image = cv.putText(image, text_to_print, (80,80), cv.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0))
            image = cv.putText(image, text_to_print_2, (80,160), cv.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0))

        ## Either accept of reject call
        if flag2 and (isRejectCall or isPickUpCall):
            if isRejectCall:
                text_to_print = 'Call Rejected'
                isRejectCall = False
            elif isPickUpCall:
                text_to_print = 'Call Accepted'
                isPickUpCall = False
            text_to_print_2 = ''
            flag2 = False
            text_print_end_time = datetime.now() + timedelta(seconds = 2)
            print('Call Responded')
            mode = 0
                

        # check if there is a hand in camera feed
        if results.multi_hand_landmarks:
            count = 0
            mhl = results.multi_hand_landmarks
            for num, hand in enumerate(results.multi_hand_landmarks):

                mp_drawing.draw_landmarks(image, hand, mp_hands.HAND_CONNECTIONS)
                all_xs = np.array([joint.x for joint in mhl[0].landmark])
                all_ys = np.array([joint.y for joint in mhl[0].landmark])
                all_zs = np.array([joint.z for joint in mhl[0].landmark])
            
                
                fing_list = collect_data.append(hand,size_list)

                ## Call has been received
                if flag2:
                    isPickUpCall, isRejectCall, isHandStraightFlatFirst, prev_x_mean = respond_call(all_xs, all_ys, isHandStraightFlatFirst, prev_x_mean)
                else:
                    if datetime.now() > text_print_end_time:
                        
                        # Recheck mode after mode timer has ended or the current mode is the base mode
                        if datetime.now() >= mode_endtime or mode == 0: 
                            
                            mode,mode_endtime = change_mode(mode, fing_list,mode_endtime,collect_data)
                            
                        text_to_print = ''
                        text_to_print_2 = ''

                        results = mp_hands_hands.process(image)

                        # all functions
                        if mode == 0:
                            #Returns the volume bar(not used in this model) and volume percentage
                            volbar, volper = volume_control(mp_hands_hands, mp_hands,mp_drawing, cap)
                            if volper > 0.5:
                                cv2.putText(image,f"{int(volper)}%",(10,40),cv2.FONT_ITALIC,1,(0, 255, 98),3)
                                #Outputs the volume percentage when the activation gesture is held.
                                image = cv2.putText(image, 'VOLUME', (80,185), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0))

                            # Check to see if next track gesture has been identified
                            text_to_print, isThumbRightFirst, prev_thumbTip_x_next, mode_endtime, flag1 = next_track(text_to_print, mode, mhl, isThumbRightFirst, prev_thumbTip_x_next, mode_endtime)
                            # If no next track gesture, then check for previous track
                            if flag1 ==0:
                                text_to_print, isThumbLeftFirst, prev_thumbTip_x_prev, mode_endtime = previous_track(text_to_print, mode, mhl, isThumbLeftFirst, prev_thumbTip_x_prev, mode_endtime)
                            
                            #returns the lengths of various fingers. When the gesture is a fist, the music is paused.
                            #once paused, remove hand momentarily and hold same gesture to play music.
                            length2, length3, length4, length5, lengtht = pause_control(mp_hands_hands, mp_hands,mp_drawing, cap)
                            if length2 < 30 and length3 < 30 and length4 < 30 and length5 < 30 and lengtht < 80:
                                if flagp == True:
                                    #outputs text when activation gesture is held. 
                                    image = cv2.putText(image, 'PAUSE MUSIC', (80,185), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 0, 0))

                                    # Allow to change to play mode
                                    changeflag = True
    
                                    
                                elif flagp == False:        
                                    image = cv2.putText(image, 'PLAY MUSIC', (80,185), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 0, 0))
                                    # Allow to change to play mode
                                    changeflag = True


                        elif mode == 1:
                            volbar = 0
                            volper = 0
                            #Returns the temperature bar(not used in this model) and temperature percentage
                            #same function is called. Outputs temperature percentage in climate mode.
                            volbar, volper = volume_control(mp_hands_hands, mp_hands,mp_drawing, cap)
                            if volper > 0.5:
                                cv2.putText(image,f"{int(volper)}%",(10,40),cv2.FONT_ITALIC,1,(0, 255, 98),3)  
                                image = cv2.putText(image, 'TEMPERATURE', (80,185), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0))
                                # Add time to timer so that mode 1 doesn't end prematurely 
                                mode_endtime = mode_endtime + timedelta(seconds = 0.2)
                            
                        if text_to_print != '':
                            #when gestures are held in this mode, the timer gets extended. 
                            # as long as the current time doesnt reach this time, the mode will stay in climate.
                            text_print_end_time = datetime.now() + timedelta(seconds = 1)
                            flag1 = 0
                        
 
        elif not flag2 and not results.multi_hand_landmarks:
            count+=1
            # If currently in pause mode and change flag is true, then switch to play mode
            if flagp == True and changeflag == True:
                flagp = False
                changeflag == False
            # If currently in play mode and change flag is true, then switch to pause mode
            elif flagp == False and changeflag == True:
                flagp = True
                changeflag == False
            # If no hand has been in the frame for a while, then automatically return to base mode
            if count >30:
                mode = 0
                text_to_print = ''
                text_to_print_2 = ''
                collect_data.clear()               
        if datetime.now() > text_print_end_time and not flag2:
            text_to_print = ''
            text_to_print_2 = ''
            text_to_print1 = "Currrent MODE:" + str(mode)
        
        image = cv.putText(image, text_to_print, (80,80), cv.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0))
        image = cv.putText(image, "Currrent MODE:" + modes_dict[mode], (20,450), cv.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0))
        image = cv.putText(image, text_to_print_2, (80,160), cv.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0))
        
        cv.imshow("output", image)


        if cv.waitKey(33) == ord('q'):
            break