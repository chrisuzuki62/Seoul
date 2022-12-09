# import libaries
import cv2 as cv
import numpy as np
import mediapipe as mp
import uuid
import os
from datetime import datetime, timedelta

# =================================================================
# change_track.py
def isthumbRight(all_xs):
    return np.argmax(all_xs) == 4

def thumbLeft(all_xs):
    return np.argmin(all_xs) == 4

def fist(all_ys):
    joints = all_ys[5:]
    return np.max(joints) - np.min(joints) < 0.25

def isSmallest(pos, pos_arr):
    return np.min(pos_arr) == pos

def isLargest(pos, pos_arr):
    return np.max(pos_arr) == pos
# =================================================================

# handle_calls.py
def isHandStraightFlat(all_xs):
    return (np.max(all_xs) - np.min(all_xs)) < 0.2

def isPickUpPhoneGesture(all_xs, all_ys):
    thumb_tip_x = all_xs[4]
    thumb_tip_y = all_ys[4]

    pinky_tip_x = all_xs[20]
 
    return isSmallest(pinky_tip_x, all_xs) and (isLargest(thumb_tip_x, all_xs) or isSmallest(thumb_tip_y, all_ys))


def test():
    print('test')

def one_two(fing_list):
    # finger_list = [thumb_xavg,thumb_yavg, ind_xavg,ind_yavg,mid_xavg,mid_yavg, ring_xavg,ring_yavg,pinky_xavg,pinky_yavg,wrist_xavg,wrist_yavg]
    print("inone")
    xdist = fing_list[2]-fing_list[4]
    ydist = fing_list[3]-fing_list[5]
    ## Calculate the distance between the index and middle finger tips
    dist_index_middle = np.sqrt(xdist**2+ydist**2)
    print(dist_index_middle)

    # Check if fingers are close to wrist
    wx = fing_list[10]
    wy = fing_list[11]
    # Thumb:
    thumb_dist = np.sqrt((fing_list[0]-wx)**2+(fing_list[1]-wy)**2)
    print("thumb:",thumb_dist)
    # index:
    ind_dist = np.sqrt((fing_list[2]-wx)**2+(fing_list[3]-wy)**2)
    print("index:",ind_dist)
    # Thumb:
    mid_dist = np.sqrt((fing_list[4]-wx)**2+(fing_list[5]-wy)**2)
    # Thumb:
    ring_dist = np.sqrt((fing_list[6]-wx)**2+(fing_list[7]-wy)**2)
    print("ring:",ring_dist)
    # Thumb:
    pinky_dist = np.sqrt((fing_list[8]-wx)**2+(fing_list[9]-wy)**2)
    print("pinky:",pinky_dist)

    thumb_middle = np.sqrt((fing_list[0]-fing_list[4])**2+(fing_list[1]-fing_list[5])**2)
    print("thumb:",thumb_middle)

    if dist_index_middle >0.085 and ind_dist > 1.5*thumb_dist and ind_dist > 1.8*ring_dist and ind_dist > 1.8*pinky_dist and ind_dist-mid_dist < 0.05:
        return (2)
    elif ind_dist > 1.5*thumb_dist and ind_dist > 1.8*ring_dist and ind_dist > 1.8*pinky_dist and ind_dist > 1.8*mid_dist and thumb_middle < 0.11:
        print("I classify as mode 1")
        return (1)
    else:
        return(0)

def change_mode(mode, fing_list, mode_endtime,collect_data):

    if len(fing_list) == 12:
## Recognize as peach if the distances are far enough   
        if one_two(fing_list) == 1:
            mode = 1
            mode_endtime = datetime.now() + timedelta(seconds = 4)
            collect_data.clear()
            print(f"mode {mode}")

            # image = cv2.putText(image, 'Peace Sign', (80,80), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 0, 0))
        # elif one_two(fing_list) == 2:
        #     mode = 2
        #     print(f"mode {mode}")
        #     print(0)
        else:
            print("IN HEREEERREERER")
            mode = 0 # = "base"

    return mode, mode_endtime