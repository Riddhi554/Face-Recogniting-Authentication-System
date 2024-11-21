import face_recognition as fr
import numpy as np
import os
import cv2
import tkinter as tk
from tkinter import filedialog, messagebox
import logging

# Configure logging for authentication events
logging.basicConfig(filename='authentication_log.txt', level=logging.INFO, 
                    format='%(asctime)s:%(levelname)s:%(message)s')

exclude_names = ['Unknown']
TOLERANCE = 0.5  # Face matching tolerance

# Encode faces and return encoding dictionary
def encode_faces():
    encoded_data = {}
    for dirpath, dnames, fnames in os.walk("./Images"):
        for f in fnames:
            if f.endswith(".jpg") or f.endswith(".png"):
                face = fr.load_image_file(f"Images/{f}")
                encoding = fr.face_encodings(face)[0]
                encoded_data[f.split(".")[0]] = encoding
    return encoded_data

# Process each frame for face recognition
def process_frame(frame, encoded_faces, faces_name):
    face_locations = fr.face_locations(frame)
    unknown_face_encodings = fr.face_encodings(frame, face_locations)

    face_names = []
    for face_encoding in unknown_face_encodings:
        matches = fr.compare_faces(encoded_faces, face_encoding, TOLERANCE)
        name = "Unknown"

        face_distances = fr.face_distance(encoded_faces, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = faces_name[best_match_index]
            logging.info(f"Authenticated: {name}")
        else:
            logging.warning("Unrecognized face detected")

        face_names.append(name)

    return face_locations, face_names

# Real-time face recognition handling for authentication
def handle_real_time():
    faces = encode_faces()
    encoded_faces = list(faces.values())
    faces_name = list(faces.keys())
    video_frame = True

    video_capture = cv2.VideoCapture(0)

    while True:
        ret, frame = video_capture.read()
        if not ret:
            logging.error("Failed to grab frame.")
            break

        if video_frame:
            face_locations, face_names = process_frame(frame, encoded_faces, faces_name)
        video_frame = not video_frame

        for (top, right, bottom, left), name in zip(face_locations, face_names):
            color = (0, 255, 0) if name != "Unknown" else (0, 0, 255)
            cv2.rectangle(frame, (left - 20, top - 20), (right + 20, bottom + 20), color, 2)
            cv2.rectangle(frame, (left - 20, bottom - 15), (right + 20, bottom + 20), color, cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, f"Authenticated: {name}" if name != "Unknown" else "Access Denied", 
                        (left - 20, bottom + 15), font, 0.85, (255, 255, 255), 2)

        cv2.imshow('Real-Time Face Authentication', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()

# Handle authentication for a group photo
def handle_group_photo(photo_path):
    faces = encode_faces()
    encoded_faces = list(faces.values())
    faces_name = list(faces.keys())

    if os.path.exists(photo_path):
        group_photo = cv2.imread(photo_path)
        face_locations, face_names = process_frame(group_photo, encoded_faces, faces_name)

        for (top, right, bottom, left), name in zip(face_locations, face_names):
            color = (0, 255, 0) if name != "Unknown" else (0, 0, 255)
            cv2.rectangle(group_photo, (left - 20, top - 20), (right + 20, bottom + 20), color, 2)
            cv2.rectangle(group_photo, (left - 20, bottom - 15), (right + 20, bottom + 20), color, cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(group_photo, f"Authenticated: {name}" if name != "Unknown" else "Access Denied", 
                        (left - 20, bottom + 15), font, 0.85, (255, 255, 255), 2)

        cv2.imshow('Group Photo Authentication', group_photo)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        messagebox.showerror("Error", "Group photo not found!")
        logging.error("Group photo not found at path: " + photo_path)

# Functions to handle button clicks
def start_real_time():
    logging.info("Starting real-time face authentication.")
    handle_real_time()

def load_group_photo():
    file_path = filedialog.askopenfilename(title="Select Group Photo", filetypes=[("Image Files", "*.jpg *.png")])
    if file_path:
        handle_group_photo(file_path)

# Creating the tkinter window
root = tk.Tk()
root.title("Face Recognition Authentication System")

# Set window size
root.geometry("400x250")

# Label
title_label = tk.Label(root, text="Face Recognition Authentication", font=("Helvetica", 16))
title_label.pack(pady=10)

# Buttons
real_time_btn = tk.Button(root, text="Start Real-Time Video", command=start_real_time, width=25)
real_time_btn.pack(pady=10)

group_photo_btn = tk.Button(root, text="Load Group Photo", command=load_group_photo, width=25)
group_photo_btn.pack(pady=10)

# Main loop
root.mainloop()
