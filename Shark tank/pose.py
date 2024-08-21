import tkinter as tk
from tkinter import Label
import cv2
from PIL import Image, ImageTk
import mediapipe as mp
import numpy as np
from tkinter import *



# Initialize MediaPipe pose model
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

class ExerciseCorrectionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Exercise Pose Correction AI Trainer")

        # Create a Label to display the video feed
        self.video_label = Label(root)
        self.video_label.pack()

        # Placeholder for feedback label
        self.feedback_label = Label(root, text="Perform a squat!")
        self.feedback_label.pack()

        # Start capturing video
        self.cap = cv2.VideoCapture(0)
        self.update_video_feed()

        # Close the app when the window is closed
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def update_video_feed(self):
        ret, frame = self.cap.read()
        if ret:
            # Convert the frame to RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Process the frame to detect pose
            results = pose.process(frame_rgb)

            if results.pose_landmarks:
                # Draw pose landmarks
                mp.solutions.drawing_utils.draw_landmarks(
                    frame_rgb, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

                # Squat exercise correction logic
                self.correct_squat(results.pose_landmarks)

            # Convert the image to display in Tkinter
            img = Image.fromarray(frame_rgb)
            imgtk = ImageTk.PhotoImage(image=img)

            self.video_label.imgtk = imgtk
            self.video_label.configure(image=imgtk)

        # Repeat after 10 milliseconds
        self.root.after(10, self.update_video_feed)

    def correct_squat(self, landmarks):
        # Extract relevant landmarks
        hip = landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP]
        knee = landmarks.landmark[mp_pose.PoseLandmark.LEFT_KNEE]
        ankle = landmarks.landmark[mp_pose.PoseLandmark.LEFT_ANKLE]

        # Calculate angles (in degrees) using the law of cosines
        hip_knee_vec = np.array([hip.x - knee.x, hip.y - knee.y])
        knee_ankle_vec = np.array([knee.x - ankle.x, knee.y - ankle.y])
        
        angle = np.arccos(np.dot(hip_knee_vec, knee_ankle_vec) / 
                          (np.linalg.norm(hip_knee_vec) * np.linalg.norm(knee_ankle_vec)))
        angle_deg = np.degrees(angle)

        # Check if the squat is deep enough (e.g., angle should be below 90 degrees)
        if angle_deg > 90:
            self.feedback_label.config(font=30,text="Good Squat!",fg="blue")
        else:
            self.feedback_label.config(font=30,text="Go lower!",fg="red")

    def on_close(self):
        self.cap.release()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = ExerciseCorrectionApp(root)
    root.mainloop()