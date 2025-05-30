import os
import sys
import django
import face_recognition
import pickle
import cv2
import requests
from datetime import datetime

# ✅ Setup Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "attendance.settings")
django.setup()

# Load encoded faces
with open('recognition/known_faces.pkl', 'rb') as f:
    data = pickle.load(f)
    known_face_encodings = data["encodings"]
    known_face_names = data["names"]
    student_ids = data["ids"]

# Load classroom ID from command line
if len(sys.argv) < 2:
    print("Usage: python face_attendance_api.py <classroom_id>")
    sys.exit(1)

classroom_id = int(sys.argv[1])

# API endpoint
API_ENDPOINT = 'http://127.0.0.1:8000/api/submit-attendance/'

# Webcam
video_capture = cv2.VideoCapture(0)

if not video_capture.isOpened():
    print("❌ Webcam access error.")
    sys.exit(1)

print("✅ Starting face recognition... Press 'q' to quit.")

seen_students = set()

while True:
    ret, frame = video_capture.read()
    if not ret:
        print("❌ Failed to read frame.")
        break

    rgb_frame = frame[:, :, ::-1]
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)

        best_match_index = None
        if matches:
            best_match_index = min(range(len(face_distances)), key=lambda i: face_distances[i])

        if best_match_index is not None and matches[best_match_index]:
            student_id = student_ids[best_match_index]
            if student_id not in seen_students:
                seen_students.add(student_id)
                data = {
                    'student_id': student_id,
                    'classroom_id': classroom_id,
                    'status': 'Present',
                    'timestamp': datetime.now().isoformat()
                }
                try:
                    response = requests.post(API_ENDPOINT, json=data)
                    if response.status_code == 200:
                        print(f"✅ Attendance logged for {known_face_names[best_match_index]}")
                    else:
                        print(f"❌ Failed to submit attendance for {known_face_names[best_match_index]}: {response.text}")
                except Exception as e:
                    print(f"❌ Error connecting to server: {e}")

    cv2.imshow('Face Attendance', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
