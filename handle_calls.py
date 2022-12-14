# import libraries
from helper_functions import *
import cv2 as cv
import numpy as np
import mediapipe as mp
import uuid
import os
from datetime import datetime, timedelta

from helper_functions import *

def respond_call(all_xs, all_ys, isHandStraightFlatFirst, prev_x_mean):

    # helper vars
    cur_x_mean = np.mean(all_xs)
    isRejectCall = False
    isPickUpCall = False

    # if last gesture is straight and flat hand and hand has moved to the right
    # print "Reject Call"
    if isHandStraightFlatFirst and (cur_x_mean - prev_x_mean) >= 0.2:
        isHandStraightFlatFirst = False
        print('Reject Call')
        isRejectCall = True

    # if "phone call" gesture is made, print "Pickup Call"
    elif isPickUpPhoneGesture(all_xs, all_ys):
        isHandStraightFlatFirst = False
        print('Pickup Call')
        isPickUpCall = True

    # see if current gesture is straight and flat hand
    elif isHandStraightFlat(all_xs):
        prev_x_mean = cur_x_mean
        isHandStraightFlatFirst = True

    return isPickUpCall, isRejectCall, isHandStraightFlatFirst, prev_x_mean