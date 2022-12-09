import cv2
import mediapipe as mp
import speech_recognition as sr
import time
from mode import *
import pyrealsense2 as rs

import numpy as np

#Information about tracking:  https://google.github.io/mediapipe/solutions/hands.html

#initialize hand recognition
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

# Configure depth and color streams from realsense camera
pipeline = rs.pipeline()
config = rs.config()

# Get device product line for setting a supporting resolution
pipeline_wrapper = rs.pipeline_wrapper(pipeline)
pipeline_profile = config.resolve(pipeline_wrapper)
device = pipeline_profile.get_device()
device_product_line = str(device.get_info(rs.camera_info.product_line))

found_rgb = False
for s in device.sensors:
    if s.get_info(rs.camera_info.name) == 'RGB Camera':
        found_rgb = True
        break
if not found_rgb:
    print("The demo requires Depth camera with Color sensor")
    exit(0)

config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.infrared, 640, 480, rs.format.y8, 30)

if device_product_line == 'L500':
    config.enable_stream(rs.stream.color, 960, 540, rs.format.bgr8, 30)
else:
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

# Start streaming
profile = pipeline.start(config)


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
  #cap = cv2.VideoCapture(0)  #comment out for realsense

  ### Create running lists for useful hand coordinates to take average and remove noise
  thumb_x = np.empty((0,20))
  thumb_y = np.empty((0,20))
  index_x = np.empty((0,20))
  index_y= np.empty((0,20))
  middle_x = np.empty((0,20))
  middle_y = np.empty((0,20))
  ring_x = np.empty((0,20))
  ring_y = np.empty((0,20))
  pinky_x = np.empty((0,20))
  pinky_y = np.empty((0,20))
  wrist_x = np.empty((0,20))
  wrist_y = np.empty((0,20))

#   middle_tip_x,middle_tip_y,index_tip_x,index_tip_y= np.empty((0,20))
  mode = "Base"
  with mp_hands.Hands(
      model_complexity=0,
      max_num_hands=1,
      min_detection_confidence=0.5,
      min_tracking_confidence=0.5) as hands:
    # while cap.isOpened():
    #   success, image = cap.read()
    #   if not success:
    #     print("Ignoring empty camera frame.")
    #     # If loading a video, use 'break' instead of 'continue'.
    #     continue
    while True:
        frames = pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()
        infrared_frame = frames.get_infrared_frame()

        if not depth_frame or not color_frame or not infrared_frame:
            continue

        # Convert images to numpy arrays
        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())
        infrared_image = np.asanyarray(infrared_frame.get_data())

        # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)

        depth_colormap_dim = depth_colormap.shape
        color_colormap_dim = color_image.shape
        infrared_colormap__dim = infrared_image.shape

        # If depth and color resolutions are different, resize color image to match depth image for display
        if depth_colormap_dim != color_colormap_dim:
            resized_color_image = cv2.resize(color_image, dsize=(depth_colormap_dim[1], depth_colormap_dim[0]), interpolation=cv2.INTER_AREA)
        
        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.      
        resized_color_image.flags.writeable = False
        resized_color_image = cv2.cvtColor(resized_color_image, cv2.COLOR_BGR2RGB)
        results = hands.process(resized_color_image)

        ## Take running average of 20 data points
        size_list = 20

        # Draw the hand annotations on the image.
        resized_color_image.flags.writeable = True
        resized_color_image = cv2.cvtColor(resized_color_image, cv2.COLOR_RGB2BGR)


        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    resized_color_image,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style())
                image_height, image_width, _ = resized_color_image.shape

            # Calculate Center of Palm
            offset = 0
            pinky_mcp_x = int(hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_MCP].x * depth_colormap_dim[1])
            pinky_mcp_y = int(hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_MCP].y * depth_colormap_dim[0]+offset)
            if pinky_mcp_x < 1:
                pinky_mcp_x = 1
            elif pinky_mcp_y < 1:    
                pinky_mcp_y = 1                    
            elif pinky_mcp_x > 639:
                pinky_mcp_x = 639
            elif pinky_mcp_y > 479:
                pinky_mcp_y = 479
            
            index_mcp_x = int(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].x * depth_colormap_dim[1])
            index_mcp_y = int(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].y * depth_colormap_dim[0]+offset)
            if index_mcp_x < 1:
                index_mcp_x = 1
            elif index_mcp_y < 1:    
                index_mcp_y = 1                    
            elif index_mcp_x > 639:
                index_mcp_x = 639
            elif index_mcp_y > 479:
                index_mcp_y = 479

            d_wrist_x = int(hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x * depth_colormap_dim[1])
            d_wrist_y = int(hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y * depth_colormap_dim[0]+offset)
            if d_wrist_x < 1:
                d_wrist_x = 1
            elif d_wrist_y < 1:    
                d_wrist_y = 1                    
            elif d_wrist_x > 639:
                d_wrist_x = 639
            elif d_wrist_y > 479:
                d_wrist_y = 479

            # Collect Distance Data
            palm_x = int((d_wrist_x + index_mcp_x + pinky_mcp_x)/3)
            palm_y = int((d_wrist_y + index_mcp_y + pinky_mcp_y)/3)
            dist = depth_frame.get_distance(palm_x, palm_y)


            ## Continue adding to the running list if length is not at size_list yet
            if len(index_x)<size_list:
                thumb_x = np.append(thumb_x,hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x)
                thumb_y = np.append(thumb_y,hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y)
                index_x = np.append(index_x,hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x)
                index_y = np.append(index_y,hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y)
                middle_x = np.append(middle_x,hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].x)
                middle_y = np.append(middle_y,hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y)
                ring_x = np.append(ring_x,hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].x)
                ring_y = np.append(ring_y,hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].y)
                pinky_x = np.append(pinky_x,hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].x)
                pinky_y = np.append(pinky_y,hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].y)
                wrist_x = np.append(wrist_x,hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x)
                wrist_y = np.append(wrist_y,hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y)

                # print(len(index_tip_x))
            
            
            ## If the size of the list is 20, then calculate the running average
            elif len(index_x) == size_list:
                thumb_xavg = np.sum(thumb_x)/size_list
                thumb_yavg = np.sum(thumb_y)/size_list
                ind_xavg = np.sum(index_x)/size_list
                ind_yavg = np.sum(index_y)/size_list
                mid_xavg = np.sum(middle_x)/size_list
                mid_yavg = np.sum(middle_y)/size_list
                ring_xavg = np.sum(ring_x)/size_list
                ring_yavg = np.sum(ring_y)/size_list
                pinky_xavg = np.sum(pinky_x)/size_list
                pinky_yavg = np.sum(pinky_y)/size_list
                wrist_xavg = np.sum(wrist_x)/size_list
                wrist_yavg = np.sum(wrist_y)/size_list
                finger_list = [thumb_xavg,thumb_yavg, ind_xavg,ind_yavg,mid_xavg,mid_yavg, ring_xavg,ring_yavg,pinky_xavg,pinky_yavg,wrist_xavg,wrist_yavg,dist]

                thumb_x = np.empty((0,20))
                thumb_y = np.empty((0,20))
                index_x = np.empty((0,20))
                index_y= np.empty((0,20))
                middle_x = np.empty((0,20))
                middle_y = np.empty((0,20))
                ring_x = np.empty((0,20))
                ring_y = np.empty((0,20))
                pinky_x = np.empty((0,20))
                pinky_y = np.empty((0,20))
                wrist_x = np.empty((0,20))
                wrist_y = np.empty((0,20))

                ## Recognize as peach if the distances are far enough
                if one_two(finger_list) == 1:
                    mode = 1
                    print(f"mode {mode}")
                    # image = cv2.putText(image, 'Peace Sign', (80,80), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 0, 0))
                elif one_two(finger_list) == 2:
                    mode = 2
                    print(f"mode {mode}")
                    print(0)
                else:
                    mode = "Base"
                    
        else:
            index_middle_x = 0
            index_middle_y = 0
            index_middle_z = 0
            d_wrist_x = 1
            d_wrist_y = 1
            index_mcp_x = 1
            index_mcp_y = 1
            pinky_mcp_x = 1
            pinky_mcp_y = 1
            palm_x = 1
            palm_y = 1
            dist = 0

        # stacking output image
        resized_color_image = cv2.circle(resized_color_image, [palm_x, palm_y], 5, [255, 0, 0], -1)   #higher value lower for y      more right
        resized_color_image = cv2.flip(resized_color_image, 1)
        resized_color_image = cv2.putText(resized_color_image, "mode "+ str(mode), (80,80), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 255))
        resized_color_image = cv2.flip(resized_color_image, 1)
        if depth_colormap_dim != color_colormap_dim:
            images = np.hstack((resized_color_image, depth_colormap))
        else:
            images = np.hstack((color_image, depth_colormap))

        # Flip the image horizontally for a selfie-view display.
        images = cv2.flip(images, 1)
    #   if peace_flag == 1:
        
        cv2.imshow('MediaPipe Hands', images)
        #Text = ST.SpeechtoText.listening
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        #elif Text in ['done', 'escape', 'exit']:
            #print('exiting')            
            # break
  #cap.release()
    else:
        print(MyText + ' is an invalid command. Please try again')







# For static images:
# IMAGE_FILES = []
# with mp_hands.Hands(
#     static_image_mode=True,    #was set to True = static image,   False = video
#     max_num_hands=1,
#     min_detection_confidence=0.5) as hands:
#   for idx, file in enumerate(IMAGE_FILES):
#     # Read an image, flip it around y-axis for correct handedness output (see
#     # above).
#     image = cv2.flip(cv2.imread(file), 1)
#     # Convert the BGR image to RGB before processing.
#     results = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

#     # Print handedness and draw hand landmarks on the image.
#     print('Handedness:', results.multi_handedness)
#     if not results.multi_hand_landmarks:
#       continue
#     image_height, image_width, _ = image.shape
#     annotated_image = image.copy()
#     for hand_landmarks in results.multi_hand_landmarks:
#       print('hand_landmarks:', hand_landmarks)
#       print(
#           f'Index finger tip coordinates: (',
#           f'{hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * image_width}, '
#           f'{hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * image_height})'
#       )
#       mp_drawing.draw_landmarks(
#           annotated_image,
#           hand_landmarks,
#           mp_hands.HAND_CONNECTIONS,
#           mp_drawing_styles.get_default_hand_landmarks_style(),
#           mp_drawing_styles.get_default_hand_connections_style())a
#     cv2.imwrite(
#         '/tmp/annotated_image' + str(idx) + '.png', cv2.flip(annotated_image, 1))
#     # Draw hand world landmarks.
#     if not results.multi_hand_world_landmarks:
#       continue
#     for hand_world_landmarks in results.multi_hand_world_landmarks:
#       mp_drawing.plot_landmarks(
#         hand_world_landmarks, mp_hands.HAND_CONNECTIONS, azimuth=5)


