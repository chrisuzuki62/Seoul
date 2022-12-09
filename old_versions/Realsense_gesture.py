import cv2
import mediapipe as mp
import time
import pyrealsense2 as rs
import numpy as np

#Information about tracking:  https://google.github.io/mediapipe/solutions/hands.html

#initialize hand recognition
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

# Configure depth and color streams
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

state = 0
MyText = 'gesture'
if MyText in ['turn on gesture recognition', 'gesture recognition', 'gesture', 'on gesture recognition']:    
    print(MyText)
    print('Turning on Gesture Recognition')
    # For webcam input:
  
  
    cap = cv2.VideoCapture(0)
    middle_tip_x = []
    middle_tip_y = []
    index_tip_x = []
    index_tip_y = []
    with mp_hands.Hands(
        model_complexity=0,
        max_num_hands=1,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as hands:

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
                #resized_infrared_image = cv2.resize(color_image, dsize=(infrared_colormap__dim[1], infrared_colormap__dim[0]), interpolation=cv2.INTER_AREA)
            
            resized_color_image.flags.writeable = False
            resized_color_image = cv2.cvtColor(resized_color_image, cv2.COLOR_BGR2RGB)
            results = hands.process(resized_color_image)

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


        # index_x = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x
        # middle_x = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].x
    #     if len(index_tip_x)<size_list:
    #       middle_tip_x.append(hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].x)
    #       middle_tip_y.append(hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y)
    #       index_tip_x.append(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x)
    #       index_tip_y.append(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y)
    #       # print(len(index_tip_x))
    #     elif len(index_tip_x) == size_list:
    #       mid_tip_xavg = sum( middle_tip_x)/size_list
    #       mid_tip_yavg = sum( middle_tip_y)/size_list
    #       ind_tip_xavg = sum( index_tip_x)/size_list
    #       ind_tip_yavg = sum( index_tip_y)/size_list
    #       index_middle_x = ind_tip_xavg - mid_tip_xavg
    #       index_middle_y = ind_tip_yavg - mid_tip_yavg
    #       middle_tip_x = []
    #       middle_tip_y = []
    #       index_tip_x = []
    #       index_tip_y = []
    #       # index_middle_z = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].z - hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].z
    #       dist_index_middle = np.sqrt(index_middle_x**2+index_middle_y**2)
          
    #       if dist_index_middle > 0.08:
    #         print('peace')
            
    #       else:
    #         print(0)
    #   else:
    #     index_middle_x = 0
    #     index_middle_y = 0
    #     index_middle_z = 0
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

                wrist_x = int(hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x * depth_colormap_dim[1])
                wrist_y = int(hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y * depth_colormap_dim[0]+offset)
                if wrist_x < 1:
                    wrist_x = 1
                elif wrist_y < 1:    
                    wrist_y = 1                    
                elif wrist_x > 639:
                    wrist_x = 639
                elif wrist_y > 479:
                    wrist_y = 479
                

            else:
                wrist_x = 1
                wrist_y = 1
                index_mcp_x = 1
                index_mcp_y = 1
                pinky_mcp_x = 1
                pinky_mcp_y = 1
                dist = 0                
            
            palm_x = int((wrist_x + index_mcp_x + pinky_mcp_x)/3)
            palm_y = int((wrist_y + index_mcp_y + pinky_mcp_y)/3)
            dist = depth_frame.get_distance(palm_x, palm_y)  #center of resolution 640/2, 480/2
            print(dist)
            
            resized_color_image = cv2.circle(resized_color_image, [palm_x, palm_y], 5, [255, 0, 0], -1)   #higher value lower for y      more right
            if depth_colormap_dim != color_colormap_dim:
                images = np.hstack((resized_color_image, depth_colormap))
            else:
                images = np.hstack((color_image, depth_colormap))
            

            # Flip the image horizontally for a selfie-view display.
            # cv2.imshow('Depth Hands', cv2.flip(depth_colormap, 1))
            # cv2.imshow('RGB Hands', cv2.flip(color_image, 1))
            cv2.imshow('Hands', cv2.flip(images, 1))
            #Text = ST.SpeechtoText.listening
            if cv2.waitKey(1) & 0xFF == ord('q') or state == 'peace':
                break
            #elif Text in ['done', 'escape', 'exit']:
                print('exiting')            
                # break
else:
    print(MyText + ' is an invalid command. Please try again')