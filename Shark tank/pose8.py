import tkinter as tk
from tkinter import Label, Button, Frame
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
        self.root.geometry("1200x700")
        self.root.configure(bg="#282C34")

        # Initial variables
        self.exercise = None
        self.rep_count = 0
        self.rep_started = False
        self.paused = False

        # Create a start page
        self.start_frame = Frame(root, bg="#61AFEF")
        self.start_frame.pack(fill="both", expand=True)
        
        Label(self.start_frame, text="Welcome to the Exercise Pose Correction AI Trainer!",
              font=("Helvetica", 20), bg="#61AFEF", fg="white").pack(pady=20)
        Button(self.start_frame, text="Start", font=("Helvetica", 14), bg="#98C379", fg="white",
               command=self.show_main_page).pack(pady=10)
        Button(self.start_frame, text="Quit", font=("Helvetica", 14), bg="#E06C75", fg="white",
               command=self.quit_app).pack(pady=10)

        # Main application page
        self.main_frame = Frame(root, bg="#282C34")
        
        self.video_label = Label(self.main_frame, bg="#282C34")
        self.video_label.pack()

        self.feedback_label = Label(self.main_frame, text="Select an exercise to start!",
                                    font=("Helvetica", 14), bg="#282C34", fg="#61AFEF")
        self.feedback_label.pack(pady=10)

        self.rep_count_label = Label(self.main_frame, text="Reps: 0", font=("Helvetica", 14),
                                     bg="#282C34", fg="#98C379")
        self.rep_count_label.pack(pady=10)

        self.control_frame = Frame(self.main_frame, bg="#282C34")
        self.control_frame.pack(pady=20)
        
        Button(self.control_frame, text="Squats",width=15,height=2, font=("Helvetica", 12), bg="#61AFEF", fg="white",
               command=self.set_exercise_squats).pack(side=tk.LEFT, )
        Button(self.control_frame, text="Pushups",width=15,height=2, font=("Helvetica", 12), bg="#61AFEF", fg="white",
               command=self.set_exercise_pushups).pack(side=tk.LEFT, )
        Button(self.control_frame, text="Lunges",width=15,height=2, font=("Helvetica", 12), bg="#61AFEF", fg="white",
               command=self.set_exercise_lunges).pack(side=tk.LEFT, )
        Button(self.control_frame, text="Planks",width=15,height=2, font=("Helvetica", 12), bg="#61AFEF", fg="white",
               command=self.set_exercise_planks).pack(side=tk.LEFT, )
        Button(self.control_frame, text="Crunches",width=15,height=2, font=("Helvetica", 12), bg="#61AFEF", fg="white",
               command=self.set_exercise_crunches).pack(side=tk.LEFT, )
        
        self.pause_button = Button(self.control_frame, text="Pause",width=15,height=2, font=("Helvetica", 12),
                                   bg="#E5C07B", fg="white", command=self.toggle_pause)
        self.pause_button.pack(side=tk.LEFT, )
        
        Button(self.control_frame, text="Quit",width=15,height=2, font=("Helvetica", 12), bg="#E06C75", fg="white",
               command=self.quit_app).pack(side=tk.LEFT,)

        # Start video capture
        self.cap = cv2.VideoCapture(0)

        # Close app on window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def show_main_page(self):
        self.start_frame.pack_forget()
        self.main_frame.pack(fill="both", expand=True)
        self.update_video_feed()

    def set_exercise_squats(self):
        self.exercise = "squats"
        self.reset()

    def set_exercise_pushups(self):
        self.exercise = "pushups"
        self.reset()

    def set_exercise_lunges(self):
        self.exercise = "lunges"
        self.reset()

    def set_exercise_planks(self):
        self.exercise = "planks"
        self.reset()

    def set_exercise_crunches(self):
        self.exercise = "crunches"
        self.reset()

    def reset(self):
        self.rep_count = 0
        self.rep_started = False
        self.feedback_label.config(text="Perform the exercise!")
        self.rep_count_label.config(text="Reps: 0")

    def toggle_pause(self):
        self.paused = not self.paused
        self.pause_button.config(text="Resume" if self.paused else "Pause")

    def update_video_feed(self):
        if not self.paused:
            ret, frame = self.cap.read()
            if ret:
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = pose.process(frame_rgb)

                if results.pose_landmarks:
                    mp.solutions.drawing_utils.draw_landmarks(
                        frame_rgb, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

                    # Apply exercise-specific logic
                    if self.exercise == "squats":
                        self.correct_and_count_squat(results.pose_landmarks)
                    elif self.exercise == "pushups":
                        self.correct_and_count_pushup(results.pose_landmarks)
                    elif self.exercise == "lunges":
                        self.correct_and_count_lunge(results.pose_landmarks)
                    elif self.exercise == "planks":
                        self.correct_and_count_plank(results.pose_landmarks)
                    elif self.exercise == "crunches":
                        self.correct_and_count_crunch(results.pose_landmarks)

                img = Image.fromarray(frame_rgb)
                imgtk = ImageTk.PhotoImage(image=img)
                self.video_label.imgtk = imgtk
                self.video_label.configure(image=imgtk)

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

        self.feedback_label.config(text="Good Pushup!" if 160 < angle > 180 else "Keep your body straight!")

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

        self.feedback_label.config(text="Good Plank!" if 160 < angle > 180 else "Keep your body straight!")

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

    def quit_app(self):
        self.cap.release()
        self.root.destroy()

    def on_close(self):
        self.quit_app()

if __name__ == "__main__":
    root = tk.Tk()
    app = ExerciseCorrectionApp(root)
    root.mainloop()
