import os
import pickle
import face_recognition
import cv2
import numpy as np
import csv
from datetime import datetime
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
import requests
from io import BytesIO
from PIL import Image

# Authenticate and build the service for Google Sheets API
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
# SERVICE_ACCOUNT_FILE = r'C:\Users\praga\OneDrive\Desktop\python\service.json'  
# # Use raw string to avoid escape issues
SERVICE_ACCOUNT_FILE = '/app/service.json'  # ✅ Linux path inside Docker


credentials = Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('sheets', 'v4', credentials=credentials)

# Replace with your Google Sheet ID
SPREADSHEET_ID = '1_hawYifDoyZ2HhjY2qaipCo3rNSdYkrgfzlMOMRRpas'  # Update with your Google Sheet ID
RANGE_NAME = 'Sheet1!A:F'  # Ensure this range includes Name, USN, Email, Gender, Department, Photo URL

# Call the Sheets API to get the data
sheet = service.spreadsheets()
result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
values = result.get('values', [])

if not values:
    print("No data found.")
else:
    known_face_encodings = []
    known_face_names = []
    student_data = {}

    # Fetch data from the sheet
    # Fetch data from the sheet
    for row in values:
        if len(row) >= 6:  # Ensure there are enough columns
            name = row[0]
            usn = row[1]
            email = row[2]
            gender = row[3]
            department = row[4]
            photo_url = row[5]

        # Skip empty or invalid photo URLs
            if not photo_url or not photo_url.startswith("https://"):
                continue  # Skip processing this row

        # Download the image from the URL
            try:
                response = requests.get(photo_url)
                response.raise_for_status()  # Raise error for bad responses
                img_data = BytesIO(response.content)
                img = Image.open(img_data).convert("RGB")  # Ensure RGB format
                img = np.array(img)
                img_rgb = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)  # Convert to BGR for OpenCV

            # Get the encoding for the image
                encoding = face_recognition.face_encodings(img_rgb)
                if encoding:
                    known_face_encodings.append(encoding[0])
                    known_face_names.append(name)
                    student_data[name] = {'usn': usn, 'email': email, 'gender': gender, 'department': department}
            except Exception:
            # Handle any errors silently to avoid terminal clutter
                continue


# Initialize webcam for face recognition
video_capture = cv2.VideoCapture(0)
if not video_capture.isOpened():
    print("Error: Could not open webcam.")
    exit()

now = datetime.now()
current_date = now.strftime("%Y-%m-%d")

# Create/Append to CSV file
f = open(f"{current_date}.csv", "a", newline="")
lnwriter = csv.writer(f)

students = known_face_names.copy()

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
            student_info = student_data.get(name, {})
            lnwriter.writerow([name, student_info.get('usn'), student_info.get('email'), student_info.get('gender'),
                               student_info.get('department'), current_time])

    cv2.imshow("Attendance", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Release resources
video_capture.release()
cv2.destroyAllWindows()
f.close()