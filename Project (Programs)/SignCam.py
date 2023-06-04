import cv2
import mediapipe as mp
import numpy as np
import torch
import pyvirtualcam as pvc

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
cap.set(cv2.CAP_PROP_FPS, 30)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

#model loading
# model = torch.hub.load('ultralytics/yolov5', 
#                        'custom', 
#                        path='modelN800/weights/best.pt' ,force_reload=True)
model = torch.hub.load('ultralytics/yolov5', 
                        'custom', 
                        path='modelS/weights/best.pt' ,force_reload=True)

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
        with pvc.Camera(width=1280, height=720, fps=30) as cam:
            while True:    
                ret, frame = cap.read()
                global letter

                # Make a copy of the original image and empty black images
                original = frame.copy()
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
                
                image = original
                start_point = (0, image.shape[0])
                end_point = (image.shape[1], image.shape[0])
                color = (0, 0, 0)
                thickness = 150
                line_type = cv2.LINE_AA
                cv2.line(image, start_point, end_point, color, thickness, line_type)    
                
                
                #print the class when 70% confidence is reached in pytorch
                for result in results.pandas().xyxy[0].iterrows():
                    if result[1]['confidence'] > 0.90:
                        #To print the class
                        name=result[1]['name']
                        ret = True
                        text = name
                        print(text)
                        
                        start_point = (0, image.shape[0])
                        end_point = (image.shape[1], image.shape[0])
                        color = (0, 0, 0)
                        thickness = 150
                        line_type = cv2.LINE_AA
                        cv2.line(image, start_point, end_point, color, thickness, line_type)
                        
                        font = cv2.FONT_HERSHEY_DUPLEX
                        fontScale = 1.5
                        color = (255,255,255)
                        thickness = 2
                        lineType = cv2.LINE_AA
                        
                        # Calculate the starting point of the text
                        (text_width, text_height), _ = cv2.getTextSize(text, font, fontScale, thickness)
                        width, height, _ = image.shape
                        x = int((width - text_width) / 2)
                        y = int((height + text_height) / 2)
                        cv2.putText(image, text, (x+250,y+40), font, fontScale, color, thickness, lineType)

                    
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)        
                cam.send(image)
                cam.sleep_until_next_frame()  
    
collectData()

cap.release()
cap.destroyAllWindows()