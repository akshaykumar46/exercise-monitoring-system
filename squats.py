import cv2
import mediapipe as mp
import numpy as np
from calculate_angle import calculate_angle

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose


def squats_fn(counter,rep_started,rep_completed,frame,pose):
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image.flags.writeable = False
    results = pose.process(image)
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    try:
        # Draw the pose landmarks on the image
        mp_drawing.draw_landmarks(
            image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        if results.pose_landmarks is not None:
            # Calculate the left and right hip, knee, and ankle angles
            left_hip = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP.value]
            right_hip = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HIP.value]
            left_knee = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_KNEE.value]
            right_knee = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_KNEE.value]
            left_ankle = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ANKLE.value]
            right_ankle = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ANKLE.value]

            left_hip_angle=[left_hip.x, left_hip.y]
            right_hip_angle=[right_hip.x, right_hip.y]
            left_knee_angle=[left_knee.x, left_knee.y]
            right_knee_angle=[right_knee.x, right_knee.y]
            left_ankle_angle=[left_ankle.x, left_ankle.y]
            right_ankle_angle=[right_ankle.x, right_ankle.y]

            # Check if a squat has started
            if not rep_started and (calculate_angle(left_hip_angle,left_knee_angle,left_ankle_angle)>100 and 
                                    calculate_angle(right_hip_angle,right_knee_angle,right_ankle_angle)>100):
                rep_started = True

            # Check if a squat has completed
            if rep_started and (calculate_angle(left_hip_angle,left_knee_angle,left_ankle_angle)<80 and 
                                    calculate_angle(right_hip_angle,right_knee_angle,right_ankle_angle)<80):
                rep_completed = True

            # Update the counter if a squat has been completed
            if rep_completed:
                counter += 1
                rep_started = False
                rep_completed = False
    except:
        pass
    
    cv2.putText(image, "Reps", (15,12), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
    cv2.putText(image, str(counter),
                (60,150),
                cv2.FONT_HERSHEY_SIMPLEX, 5, (0,0,0), 2, cv2.LINE_AA)
    
    return image,counter,rep_started,rep_completed

if __name__ == "__main__":
    print("function not called")


