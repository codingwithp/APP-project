from flask import Flask, jsonify, render_template
import cv2
import face_recognition
import numpy as np
import csv
from datetime import datetime
from io import BytesIO
from PIL import Image
import requests

app = Flask(__name__)

# Your facial recognition logic here
known_face_encodings = []
known_face_names = []
students = []

# Load known face data (replace this with your Google Sheets API logic if necessary)
def load_known_faces():
    # Add your logic to fetch and encode faces from your Google Sheets or other sources
    pass

@app.route('/')
def index():
    return render_template('index.html')  # Homepage

@app.route('/mark-attendance')
def mark_attendance():
    return render_template('mark-attendance.html')  # Facial recognition page

@app.route('/start-recognition', methods=['GET'])
def start_recognition():
    video_capture = cv2.VideoCapture(0)
    if not video_capture.isOpened():
        return jsonify({"success": False, "message": "Error: Could not open webcam."})

    now = datetime.now()
    current_date = now.strftime("%Y-%m-%d")

    # Create/Append to CSV file
    with open(f"{current_date}.csv", "a", newline="") as f:
        lnwriter = csv.writer(f)

        while True:
            _, frame = video_capture.read()
            if not _:
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

                # Mark attendance
                if name and name in students:
                    students.remove(name)
                    current_time = datetime.now().strftime("%H:%M:%S")
                    lnwriter.writerow([name, current_time])

                    # Release resources and stop processing
                    video_capture.release()
                    cv2.destroyAllWindows()
                    return jsonify({"success": True, "message": f"Attendance marked for {name}"})

            # Break loop on 'q' key
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    # Release resources
    video_capture.release()
    cv2.destroyAllWindows()

    return jsonify({"success": False, "message": "No faces recognized."})

if __name__ == "__main__":
    load_known_faces()  # Load known faces before starting the server
    app.run(debug=True)
