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