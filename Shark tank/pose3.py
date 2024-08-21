import tkinter as tk
from tkinter import Label, Button
import cv2
from PIL import Image, ImageTk
import mediapipe as mp
import numpy as np

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

        # Placeholder for feedback label and rep count
        self.feedback_label = Label(root, text="Select an exercise to start!")
        self.feedback_label.pack()
        self.rep_count_label = Label(root, text="Reps: 0")
        self.rep_count_label.pack()

        # Exercise selection buttons
        Button(root, text="Squats", command=self.set_exercise_squats).pack(side=tk.LEFT)
        Button(root, text="Pushups", command=self.set_exercise_pushups).pack(side=tk.LEFT)
        Button(root, text="Lunges", command=self.set_exercise_lunges).pack(side=tk.LEFT)
        Button(root, text="Planks", command=self.set_exercise_planks).pack(side=tk.LEFT)
        Button(root, text="Crunches", command=self.set_exercise_crunches).pack(side=tk.LEFT)

        # Start capturing video
        self.cap = cv2.VideoCapture(0)
        self.exercise = None  # Current exercise
        self.rep_count = 0  # Repetition count
        self.rep_started = False  # To track if a rep has started
        self.failed_pushups = 0  # Count of failed pushup attempts
        self.switch_to_knee_pushups = False  # Flag to switch to knee pushups
        self.update_video_feed()

        # Close the app when the window is closed
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def set_exercise_squats(self):
        self.exercise = "squats"
        self.rep_count = 0
        self.rep_started = False
        self.feedback_label.config(text="Perform a squat!")
        self.rep_count_label.config(text="Reps: 0")

    def set_exercise_pushups(self):
        self.exercise = "pushups"
        self.rep_count = 0
        self.rep_started = False
        self.failed_pushups = 0
        self.switch_to_knee_pushups = False
        self.feedback_label.config(text="Perform a pushup!")
        self.rep_count_label.config(text="Reps: 0")

    def set_exercise_lunges(self):
        self.exercise = "lunges"
        self.rep_count = 0
        self.rep_started = False
        self.feedback_label.config(text="Perform a lunge!")
        self.rep_count_label.config(text="Reps: 0")

    def set_exercise_planks(self):
        self.exercise = "planks"
        self.rep_count = 0
        self.rep_started = False
        self.feedback_label.config(text="Hold the plank position!")
        self.rep_count_label.config(text="Reps: 0")

    def set_exercise_crunches(self):
        self.exercise = "crunches"
        self.rep_count = 0
        self.rep_started = False
        self.feedback_label.config(text="Perform a crunch!")
        self.rep_count_label.config(text="Reps: 0")

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

                # Apply the exercise-specific correction and counting logic
                if self.exercise == "squats":
                    self.correct_and_count_squat(results.pose_landmarks)
                elif self.exercise == "pushups":
                    if not self.switch_to_knee_pushups:
                        self.correct_and_count_pushup(results.pose_landmarks)
                    else:
                        self.correct_and_count_knee_pushup(results.pose_landmarks)
                elif self.exercise == "lunges":
                    self.correct_and_count_lunge(results.pose_landmarks)
                elif self.exercise == "planks":
                    self.correct_and_count_plank(results.pose_landmarks)
                elif self.exercise == "crunches":
                    self.correct_and_count_crunch(results.pose_landmarks)

            # Convert the image to display in Tkinter
            img = Image.fromarray(frame_rgb)
            imgtk = ImageTk.PhotoImage(image=img)

            self.video_label.imgtk = imgtk
            self.video_label.configure(image=imgtk)

        # Repeat after 10 milliseconds
        self.root.after(10, self.update_video_feed)

    def correct_and_count_squat(self, landmarks):
        hip = landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP]
        knee = landmarks.landmark[mp_pose.PoseLandmark.LEFT_KNEE]
        ankle = landmarks.landmark[mp_pose.PoseLandmark.LEFT_ANKLE]

        angle = self.calculate_angle(hip, knee, ankle)
        if angle < 90 and not self.rep_started:
            self.rep_started = True
        if angle >= 160 and self.rep_started:
            self.rep_count += 1
            self.rep_started = False
            self.rep_count_label.config(text=f"Reps: {self.rep_count}")

        self.feedback_label.config(text="Good Squat!" if angle < 90 else "Bend your knees more!")

    def correct_and_count_pushup(self, landmarks):
        shoulder = landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER]
        hip = landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP]
        ankle = landmarks.landmark[mp_pose.PoseLandmark.LEFT_ANKLE]

        angle = self.calculate_angle(shoulder, hip, ankle)
        if angle < 90 and not self.rep_started:
            self.rep_started = True
        if angle >= 160 and self.rep_started:
            self.rep_count += 1
            self.rep_started = False
            self.rep_count_label.config(text=f"Reps: {self.rep_count}")
            self.failed_pushups = 0  # Reset failed pushups count after a successful rep
        else:
            self.failed_pushups += 1

        if self.rep_count < 10 and self.failed_pushups >= 3:
            self.switch_to_knee_pushups = True
            self.feedback_label.config(text="Switching to knee pushups! Keep going!")

        if not self.switch_to_knee_pushups:
            self.feedback_label.config(text="Good Pushup!" if 160 < angle < 180 else "Keep your body straight!")

    def correct_and_count_knee_pushup(self, landmarks):
        shoulder = landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER]
        hip = landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP]
        knee = landmarks.landmark[mp_pose.PoseLandmark.LEFT_KNEE]

        angle = self.calculate_angle(shoulder, hip, knee)
        if angle < 90 and not self.rep_started:
            self.rep_started = True
        if angle >= 160 and self.rep_started:
            self.rep_count += 1
            self.rep_started = False
            self.rep_count_label.config(text=f"Reps: {self.rep_count}")

        self.feedback_label.config(text="Good Knee Pushup!" if 160 < angle < 180 else "Keep your body straight!")

    def correct_and_count_lunge(self, landmarks):
        hip = landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP]
        knee = landmarks.landmark[mp_pose.PoseLandmark.LEFT_KNEE]
        ankle = landmarks.landmark[mp_pose.PoseLandmark.LEFT_ANKLE]

        angle = self.calculate_angle(hip, knee, ankle)
        if angle < 90 and not self.rep_started:
            self.rep_started = True
        if angle >= 160 and self.rep_started:
            self.rep_count += 1
            self.rep_started = False
            self.rep_count_label.config(text=f"Reps: {self.rep_count}")

        self.feedback_label.config(text="Good Lunge!" if angle < 90 else "Lower your body more!")

    def correct_and_count_plank(self, landmarks):
        shoulder = landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER]
        hip = landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP]
        ankle = landmarks.landmark[mp_pose.PoseLandmark.LEFT_ANKLE]

        angle = self.calculate_angle(shoulder, hip, ankle)
        if angle < 90 and not self.rep_started:
            self.rep_started = True
        if angle >= 160 and self.rep_started:
            self.rep_count += 1
            self.rep_started = False
            self.rep_count_label.config(text=f"Reps: {self.rep_count}")

        self.feedback_label.config(text="Good Plank!" if 160 < angle < 180 else "Keep your body straight!")

    def correct_and_count_crunch(self, landmarks):
        shoulder = landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER]
        hip = landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP]
        knee = landmarks.landmark[mp_pose.PoseLandmark.LEFT_KNEE]

        angle = self.calculate_angle(shoulder, hip, knee)
        if angle < 45 and not self.rep_started:
            self.rep_started = True
        if angle >= 160 and self.rep_started:
            self.rep_count += 1
            self.rep_started = False
            self.rep_count_label.config(text=f"Reps: {self.rep_count}")

        self.feedback_label.config(text="Good Crunch!" if angle < 45 else "Curl up more!")

    def calculate_angle(self, point1, point2, point3):
        a = np.array([point1.x, point1.y])
        b = np.array([point2.x, point2.y])
        c = np.array([point3.x, point3.y])

        radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
        angle = np.abs(radians * 180.0 / np.pi)

        if angle > 180.0:
            angle = 360 - angle

        return angle

    def on_close(self):
        self.cap.release()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = ExerciseCorrectionApp(root)
    root.mainloop()
