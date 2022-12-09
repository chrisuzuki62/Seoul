# import libraries
from helper_functions import *
import cv2 as cv
import numpy as np
import mediapipe as mp
import uuid
import os
from datetime import datetime, timedelta


def next_track(text_to_print, mode, positions, isThumbRightFirst, prev_thumbTip_x_next,mode_endtime):

    # if there is already another feature happening, just return the inputted values and exit function
    if text_to_print != '':
        flag1 = 0
        return text_to_print, isThumbRightFirst, prev_thumbTip_x_next, mode_endtime, flag1

    prev_thumbTip_x = prev_thumbTip_x_next

    # helper vars
    thumbLeftFirst = False
    text_to_print = ''
    next_track_dict = {0: 'Next Track', 1: 'Increase Temp'}
    
    # DUMMY
    mhl = positions

    # define finger position coordinates
    index_tip_y = mhl[0].landmark[8].y
    thumb_tip_x = mhl[0].landmark[4].x
    all_xs = np.array([joint.x for joint in mhl[0].landmark])
    all_ys = np.array([joint.y for joint in mhl[0].landmark])
    all_zs = np.array([joint.z for joint in mhl[0].landmark])


    
    # if hand is a fist+thumb to the right, and if the previous gesture is also the same
    # and if the current x coordinate of the thumb tip is > previous x coordinate of thumb tip
    # print "Next Track"
    if isthumbRight(all_xs) and isThumbRightFirst and (thumb_tip_x - prev_thumbTip_x > 0.2):
        text_to_print = next_track_dict[int(mode)]
        isThumbRightFirst = False
        prev_thumbTip_x = -1
        mode_endtime = mode_endtime + timedelta(seconds = 2)
        flag1 = 1
        print("ADDED TIME")

    # see if current gesture is thumb to the right
    elif isthumbRight(all_xs):
        text_to_print = ''
        isThumbRightFirst = True
        prev_thumbTip_x = mhl[0].landmark[4].x
        flag1 = 0
    else:
        text_to_print = ''
        isThumbRightFirst = False
        prev_thumbTip_x = -1
        flag1 = 0
        
    return text_to_print, isThumbRightFirst, prev_thumbTip_x, mode_endtime, flag1




def previous_track(text_to_print, mode, positions, isThumbLeftFirst, prev_thumbTip_x_prev, mode_endtime):

    # if there is already another feature happening, just return the inputted values and exit function
    if text_to_print != '':
        return text_to_print, isThumbLeftFirst, prev_thumbTip_x_prev

    

    # helper vars
    prev_thumbTip_x = prev_thumbTip_x_prev
    prev_track_dict = {0: 'Previous Track', 1: 'Decrease Temp'}

    # DUMMY
    mhl = positions

    # define position coordinates
    thumb_tip_x = mhl[0].landmark[4].x
    all_xs = np.array([joint.x for joint in mhl[0].landmark])
    all_ys = np.array([joint.y for joint in mhl[0].landmark])
    all_zs = np.array([joint.z for joint in mhl[0].landmark])


    # if hand is a fist+thumb to the left, and if the previous gesture is also the same
    # and if the previous x coordinate of the thumb tip is > current x coordinate of thumb tip
    # print "Previous Track"
    if thumbLeft(all_xs) and isThumbLeftFirst and (prev_thumbTip_x - thumb_tip_x > 0.2) and fist(all_ys):
        text_to_print = prev_track_dict[int(mode)]
        isThumbLeftFirst = False
        prev_thumbTip_x = -1
        mode_endtime = mode_endtime + timedelta(seconds = 2)
        print("ADDED TIME")

    # check if current hand is fist+thumb to the left
    elif thumbLeft(all_xs) and fist(all_ys):
        text_to_print = ''
        isThumbLeftFirst = True
        prev_thumbTip_x = mhl[0].landmark[4].x

    else:
        text_to_print = ''
        isThumbLeftFirst = False
        prev_thumbTip_x = -1

    return text_to_print, isThumbLeftFirst, prev_thumbTip_x,mode_endtime