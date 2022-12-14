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

# handle_calls
isHandStraightFlatFirst = False
call_awaiting_response = False
prev_x_mean = -1
isRejectCall = False
isPickUpCall = False

# mode
mode = 0 #DUMMY
flag1 = False
flag2 = False
size_list = 20
mode_endtime = datetime.now()

all_printable_texts = ['Next Track', 'Previous Track', 'Next Temp?', 'Previous Temp?']

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

        
        if cv.waitKey(33) == ord('c'):
            print('Getting a call')
            mode = 2
            flag2 = True
            start_time = datetime.now()
            text_to_print =  'Incoming Call from'
            text_to_print_2 = 'Kenji Shimada'
            image = cv.putText(image, text_to_print, (80,80), cv.FONT_HERSHEY_COMPLEX, 2, (255, 0, 0))
            image = cv.putText(image, text_to_print_2, (80,160), cv.FONT_HERSHEY_COMPLEX, 2, (255, 0, 0))
        
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
            mhl = results.multi_hand_landmarks
            for num, hand in enumerate(results.multi_hand_landmarks):

                mp_drawing.draw_landmarks(image, hand, mp_hands.HAND_CONNECTIONS)
                all_xs = np.array([joint.x for joint in mhl[0].landmark])
                all_ys = np.array([joint.y for joint in mhl[0].landmark])
                all_zs = np.array([joint.z for joint in mhl[0].landmark])
            
                # print('All_Xs', all_xs)
                # print('RES', isPickUpPhoneGesture(all_xs, all_ys))
                
                fing_list = collect_data.append(hand,size_list)
                # call has been received
                if flag2:
                #     call_awaiting_response = True
                    isPickUpCall, isRejectCall, isHandStraightFlatFirst, prev_x_mean = respond_call(all_xs, all_ys, isHandStraightFlatFirst, prev_x_mean)
                else:
                    if datetime.now() > text_print_end_time:
                        # mode_time = datetime.now()+timedelta(seconds = 5)
                        if datetime.now() >= mode_endtime or mode == 0: 
                            mode,mode_endtime = change_mode(mode, fing_list,mode_endtime)
                        
                        text_to_print = ''
                        text_to_print_2 = ''

                        # all functions
                        text_to_print, isThumbRightFirst, prev_thumbTip_x_next = next_track(text_to_print, mode, mhl, isThumbRightFirst, prev_thumbTip_x_next)
                        text_to_print, isThumbLeftFirst, prev_thumbTip_x_prev = previous_track(text_to_print, mode, mhl, isThumbLeftFirst, prev_thumbTip_x_prev)

                        # print(text_to_print, isThumbLeftFirst, isThumbRightFirst, prev_thumbTip_x_next, prev_thumbTip_x_prev)
                        if text_to_print in all_printable_texts:
                            text_print_end_time = datetime.now() + timedelta(seconds = 2)
                                #image = cv.putText(image, text_to_print, (80,80), cv.FONT_HERSHEY_COMPLEX, 2, (255, 0, 0))
                        
                # uncomment to test frame by frame
                #cv.waitKey(0)
                        
        if datetime.now() > text_print_end_time and not flag2:
            text_to_print = ''
            text_to_print_2 = ''

        text_to_print = text_to_print + "Currrent MODE:" + str(mode)
        # text_to_print_2 = text_to_print_2 + "Currrent MODE:" + str(mode)
        image = cv.putText(image, text_to_print, (80,80), cv.FONT_HERSHEY_COMPLEX, 2, (255, 0, 0))
        image = cv.putText(image, text_to_print_2, (80,160), cv.FONT_HERSHEY_COMPLEX, 2, (255, 0, 0))
        cv.imshow('Image', image)

                # ======================================================
                # determine mode using mode.py

                # ======================================================

        if cv.waitKey(33) == ord('q'):
            break