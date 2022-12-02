import cv2
import mediapipe as mp
#import speech_recognition as sr
import time
from mode_no_rs import *
import datacollect

import numpy as np
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

collect_data = datacollect.data()
#Information about tracking:  https://google.github.io/mediapipe/solutions/hands.html

# Initialize the recognizer
# r = sr.Recognizer()

# with sr.Microphone() as source2:

# wait for a second to let the recognizer
# adjust the energy threshold based on the surrounding noise level
# r.adjust_for_ambient_noise(source2, duration=0.2)
    # listens for user's inpit
#audio2 = r.listen(source2)
    # Using google to recognize audio
#MyText = r.recognize_google(audio2)
#MyText = MyText.lower()
MyText = 'gesture'
if MyText in ['turn on gesture recognition', 'gesture recognition', 'gesture', 'on gesture recognition']:    
  print(MyText)
  print('Turning on Gesture Recognition')
  # For webcam input:
  cap = cv2.VideoCapture(0)

  ### Create running lists for useful hand coordinates to take average and remove noise

  mode = "Base"
  with mp_hands.Hands(
      model_complexity=0,
      max_num_hands=1,
      min_detection_confidence=0.5,
      min_tracking_confidence=0.5) as hands:
    while cap.isOpened():
      success, image = cap.read()
      if not success:
        print("Ignoring empty camera frame.")
        # If loading a video, use 'break' instead of 'continue'.
        continue

      # To improve performance, optionally mark the image as not writeable to
      # pass by reference.
      image.flags.writeable = False
      image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
      results = hands.process(image)

      ## Take running average of 20 data points
      size_list = 30

      # Draw the hand annotations on the image.
      image.flags.writeable = True
      image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
  
      if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
          mp_drawing.draw_landmarks(
              image,
              hand_landmarks,
              mp_hands.HAND_CONNECTIONS,
              mp_drawing_styles.get_default_hand_landmarks_style(),
              mp_drawing_styles.get_default_hand_connections_style())
          image_height, image_width, _ = image.shape
          # collect_data = data()
          fing_list = collect_data.append(hand_landmarks,size_list)
          
          if len(fing_list) == 12:
          ## Recognize as peach if the distances are far enough
              if one_two(fing_list) == 1:
                  mode = 1
                  print(f"mode {mode}")
                  # image = cv2.putText(image, 'Peace Sign', (80,80), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 0, 0))
              elif one_two(fing_list) == 2:
                  mode = 2
                  print(f"mode {mode}")
                  print(0)
              else:
                  mode = "Base"
                
      else:
            mode = "Base"

      # Flip the image horizontally for a selfie-view display.
      image = cv2.flip(image, 1)
    #   if peace_flag == 1:
      image = cv2.putText(image, "mode "+ str(mode), (80,80), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 255))
      cv2.imshow('MediaPipe Hands', image)
      #Text = ST.SpeechtoText.listening
      if cv2.waitKey(1) & 0xFF == ord('q'):
        break
      #elif Text in ['done', 'escape', 'exit']:
        print('exiting')            
        # break
  cap.release()
else:
  print(MyText + ' is an invalid command. Please try again')

