import cv2
import mediapipe as mp
import numpy as np
from calculate_angle import calculate_angle


mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose


def pullups_fn(counter,is_counting,rep_completed,image,pose):
        
        image = cv2.flip(image, 1)
        # Convert the image to RGB
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        # Detect the pose in the image
        results = pose.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        try:
            # Draw the pose landmarks on the image
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            # Check if the person is doing a pull-up
            if results.pose_landmarks is not None:
                left_shoulder = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
                right_shoulder = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
                left_elbow = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ELBOW.value]
                right_elbow = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ELBOW.value]
                left_wrist = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST.value]
                right_wrist = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST.value]

                # Calculate the angle between the shoulders and elbows
                left_shoulder=[left_shoulder.x, left_shoulder.y]
                left_elbow=[left_elbow.x, left_elbow.y]
                left_wrist=[left_wrist.x, left_wrist.y]

                right_shoulder=[right_shoulder.x, right_shoulder.y]
                right_elbow=[right_elbow.x, right_elbow.y]
                right_wrist=[right_wrist.x, right_wrist.y]


                left_angle = calculate_angle(
                    left_shoulder, left_elbow, left_wrist)
                right_angle = calculate_angle(
                    right_shoulder, right_elbow, right_wrist)
                # print(left_angle, right_angle)
                # Check if the angles indicate a pull-up
                if left_angle < 90 and right_angle < 90:
                    if not is_counting:
                        is_counting = True

                if (not rep_completed) and is_counting and left_angle > 160 and right_angle > 160:
                    counter += 1
                    rep_completed = True
                    is_counting = False
                else:
                    rep_completed = False
                
        except:
             pass
        
        cv2.putText(image, "Reps", (15,12), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
        cv2.putText(image, str(counter),
                    (60,150),
                    cv2.FONT_HERSHEY_SIMPLEX, 5, (0,0,0), 2, cv2.LINE_AA)
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2),
                                mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2))  
        return image, counter,is_counting,rep_completed

if __name__ == "__main__":
    print("function not called")