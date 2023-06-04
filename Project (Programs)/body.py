import cv2
import mediapipe as mp
import numpy as np
import torch

#create mediapipe instance
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_holistic = mp.solutions.holistic

#initialize mediapipe instance
holistic = mp_holistic.Holistic(
    min_detection_confidence=0.3,
    min_tracking_confidence=0.3)

# #initialize webcam

cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)

model = torch.hub.load('ultralytics/yolov5', 
                       'custom', 
                       path='signLang/weights/best.pt' ,force_reload=True)

# Draw landmarks on the image
def draw_landmarks(image, results):
    # Drawing landmarks for left hand
    mp_drawing.draw_landmarks(
            image, 
            results.left_hand_landmarks, 
            mp_holistic.HAND_CONNECTIONS, 
            mp_drawing_styles.get_default_hand_landmarks_style())

    # Drawing landmarks for right hand
    mp_drawing.draw_landmarks(
            image, 
            results.right_hand_landmarks, 
            mp_holistic.HAND_CONNECTIONS, 
            mp_drawing_styles.get_default_hand_landmarks_style())

    #Drawing landmarks for pose
    mp_drawing.draw_landmarks(
            image, 
            results.pose_landmarks, 
            mp_holistic.POSE_CONNECTIONS, 
            mp_drawing_styles.get_default_pose_landmarks_style())

    return image

letter = ""
offset = 1

#collect data
def collectData():
    ret, frame = cap.read()
    global letter

    # Make a copy of the original image and empty black images
    original = frame.copy()
    crop_bg = np.zeros(frame.shape, dtype=np.uint8)
    black = np.zeros(frame.shape, dtype=np.uint8)
    
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image.flags.writeable = False

    # Holistic of the given image is stored in result variable
    results = holistic.process(image)

    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        

    # Draw landmarks on the image
    draw_landmarks(image, results)
    draw_landmarks(black, results)

    
    # Show output of the image with landmarks
    results = model(black)
    pred_img = np.squeeze(results.render())
    
    #crop the predicted image bbox from the pytorch result
    #print the class when 70% confidence is reached in pytorch
    for result in results.pandas().xyxy[0].iterrows():
        if result[1]['confidence'] > 0.8:
            
            #To get the coordinates of the bounding box
            x1 = int(result[1]['xmin'])-offset
            y1 = int(result[1]['ymin'])-offset
            x2 = int(result[1]['xmax'])+offset
            y2 = int(result[1]['ymax'])+offset 
            
            #To prevent the coordinates from going out of bounds
            if x1 < 0 or y1 < 0 or x2 < 0 or y2 < 0:
                x1 = int(result[1]['xmin'])
                y1 = int(result[1]['ymin'])
                x2 = int(result[1]['xmax'])
                y2 = int(result[1]['ymax'])
            
            #To crop the image
            crop_img = pred_img[y1:y2, x1:x2]
            crop_bg[y1:y2, x1:x2] = crop_img
            
            #To print the class
            name=result[1]['name']
            ret = True
            return image, pred_img,original,crop_bg,name
    return image, pred_img,original,crop_bg,letter

