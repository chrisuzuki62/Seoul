import numpy as np
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

class data():
    size_list = 20
    finger_list = []
    def __init__(self):
        self.thumb_x = np.empty((0,20))
        self.thumb_y = np.empty((0,20))
        self.index_x = np.empty((0,20))
        self.index_y= np.empty((0,20))
        self.middle_x = np.empty((0,20))
        self.middle_y = np.empty((0,20))
        self.ring_x = np.empty((0,20))
        self.ring_y = np.empty((0,20))
        self.pinky_x = np.empty((0,20))
        self.pinky_y = np.empty((0,20))
        self.wrist_x = np.empty((0,20))
        self.wrist_y = np.empty((0,20))
        self.fing_list = []
    def append(self, hand_landmarks,size_list):
        if len(self.index_x) < size_list:
            self.thumb_x = np.append(self.thumb_x,hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x)
            self.thumb_y = np.append(self.thumb_y,hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y)
            self.index_x = np.append(self.index_x,hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x)
            self.index_y = np.append(self.index_y,hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y)
            self.middle_x = np.append(self.middle_x,hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].x)
            self.middle_y = np.append(self.middle_y,hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y)
            self.ring_x = np.append(self.ring_x,hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].x)
            self.ring_y = np.append(self.ring_y,hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].y)
            self.pinky_x = np.append(self.pinky_x,hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].x)
            self.pinky_y = np.append(self.pinky_y,hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].y)
            self.wrist_x = np.append(self.wrist_x,hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x)
            self.wrist_y = np.append(self.wrist_y,hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y)
            return []
        else:
            thumb_xavg = np.sum(self.thumb_x)/size_list
            thumb_yavg = np.sum(self.thumb_y)/size_list
            ind_xavg = np.sum(self.index_x)/size_list
            ind_yavg = np.sum(self.index_y)/size_list
            mid_xavg = np.sum(self.middle_x)/size_list
            mid_yavg = np.sum(self.middle_y)/size_list
            ring_xavg = np.sum(self.ring_x)/size_list
            ring_yavg = np.sum(self.ring_y)/size_list
            pinky_xavg = np.sum(self.pinky_x)/size_list
            pinky_yavg = np.sum(self.pinky_y)/size_list
            wrist_xavg = np.sum(self.wrist_x)/size_list
            wrist_yavg = np.sum(self.wrist_y)/size_list
            self.fing_list = [thumb_xavg,thumb_yavg, ind_xavg,ind_yavg,mid_xavg,mid_yavg, ring_xavg,ring_yavg,pinky_xavg,pinky_yavg,wrist_xavg,wrist_yavg]
            self.thumb_x = np.empty((0,20))
            self.thumb_y = np.empty((0,20))
            self.index_x = np.empty((0,20))
            self.index_y= np.empty((0,20))
            self.middle_x = np.empty((0,20))
            self.middle_y = np.empty((0,20))
            self.ring_x = np.empty((0,20))
            self.ring_y = np.empty((0,20))
            self.pinky_x = np.empty((0,20))
            self.pinky_y = np.empty((0,20))
            self.wrist_x = np.empty((0,20))
            self.wrist_y = np.empty((0,20))
            return self.fing_list
    def clear(self):
        self.thumb_x = np.empty((0,20))
        self.thumb_y = np.empty((0,20))
        self.index_x = np.empty((0,20))
        self.index_y= np.empty((0,20))
        self.middle_x = np.empty((0,20))
        self.middle_y = np.empty((0,20))
        self.ring_x = np.empty((0,20))
        self.ring_y = np.empty((0,20))
        self.pinky_x = np.empty((0,20))
        self.pinky_y = np.empty((0,20))
        self.wrist_x = np.empty((0,20))
        self.wrist_y = np.empty((0,20))
