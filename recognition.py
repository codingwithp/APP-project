import face_recognition
import cv2
import numpy as np
import csv
from datetime import datetime

video_capture = cv2.VideoCapture(0)

if not video_capture.isOpened():
    print("Error: Could not open webcam.")
    exit()

# Load Known Faces
try:
    Pragathi_image = face_recognition.load_image_file("faces/Pragathi.jpg")
    Pragathi_encoding = face_recognition.face_encodings(Pragathi_image)[0]
except Exception as e:
    print("Error loading Pragathi.jpg:", e)
    exit()

try:
    Rashmitha_image = face_recognition.load_image_file("faces/Rashmitha.jpg")
    Rashmitha_encoding = face_recognition.face_encodings(Rashmitha_image)[0]
except Exception as e:
    print("Error loading Rashmitha.jpg:", e)
    exit()
try:
    Preeti_image = face_recognition.load_image_file("faces/Preeti.jpg")
    Preeti_encoding = face_recognition.face_encodings(Preeti_image)[0]
except Exception as e:
    print("Error loading Preeti.jpg:", e)
    exit()

# Known face encodings and names
known_face_encodings = [Pragathi_encoding, Rashmitha_encoding,Preeti_encoding]
known_face_names = ["Pragathi", "Rashmitha","Preeti"]

# List of expected students
students = known_face_names.copy()
now = datetime.now()
current_date = now.strftime("%Y-%m-%d")

# Create/Append to CSV file
f = open(f"{current_date}.csv", "a", newline="")
lnwriter = csv.writer(f)

while True:
    _, frame = video_capture.read()
    if not _:
        print("Error: Failed to capture frame from webcam.")
        break

    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    # Recognize faces
    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        face_distance = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distance)

        name = None
        if matches[best_match_index]:
            name = known_face_names[best_match_index]

        # Attendance
        if name and name in students:
            font = cv2.FONT_HERSHEY_SIMPLEX
            bottomLeftCornerOfText = (10, 100)
            fontScale = 1.5
            fontColor = (255, 0, 0)
            thickness = 3
            lineType = 2

            cv2.putText(frame, name + " Present", bottomLeftCornerOfText, font, fontScale, fontColor, thickness, lineType)
            students.remove(name)
            current_time = datetime.now().strftime("%H-%M-%S")
            lnwriter.writerow([name, current_time])

    cv2.imshow("Attendance", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Release resources
video_capture.release()
cv2.destroyAllWindows()
