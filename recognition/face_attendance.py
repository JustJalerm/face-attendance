import os
import sys
import django
import cv2
import numpy as np
import face_recognition
from datetime import date

# UI Button configuration
button_coords = (20, 20, 200, 70)  # (x1, y1, x2, y2)
button_text = "📸 Log Attendance"
clicked = False

# Setup Django
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "face_attendance.settings")
django.setup()

from accounts.models import StudentProfile
from classroom.models import Classroom
from attendance.models import AttendanceRecord

# Get classroom ID from CLI
try:
    classroom_id = int(sys.argv[1])
except (IndexError, ValueError):
    print("❌ No classroom ID passed.")
    exit()

# Load known faces
def load_known_faces(classroom_id):
    known_face_encodings = []
    known_face_names = []
    classroom = Classroom.objects.get(id=classroom_id)
    students = classroom.students.all()

    for student in students:
        if student.profile_image:
            image_path = os.path.join(BASE_DIR, 'media', student.profile_image.name)
            if not os.path.exists(image_path):
                print(f"⚠️ File not found: {image_path}")
                continue
            image = face_recognition.load_image_file(image_path)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            encodings = face_recognition.face_encodings(image)
            if encodings:
                known_face_encodings.append(encodings[0])
                known_face_names.append(student.user.username)
                print(f"✅ Loaded face for {student.user.username}")
            else:
                print(f"⚠️ No face found for {student.user.username}")
    return known_face_encodings, known_face_names

# Log attendance
def log_attendance(names, classroom_id):
    classroom = Classroom.objects.get(id=classroom_id)
    today = date.today()
    logged = []
    for username in names:
        student = StudentProfile.objects.get(user__username=username)
        record, created = AttendanceRecord.objects.get_or_create(
            student=student,
            classroom=classroom,
            timestamp__date=today,
            defaults={'status': 'Present'}
        )
        if created:
            print(f"✅ Logged attendance: {username}")
            logged.append(username)
        else:
            print(f"⚠️ Already logged: {username}")
    return logged

# Handle button click
def handle_click(event, x, y, flags, param):
    global clicked
    x1, y1, x2, y2 = button_coords
    if event == cv2.EVENT_LBUTTONDOWN and x1 <= x <= x2 and y1 <= y <= y2:
        clicked = True

# Face recognition
def recognize_faces():
    global clicked
    known_face_encodings, known_face_names = load_known_faces(classroom_id)
    video_capture = cv2.VideoCapture(0)

    if not video_capture.isOpened():
        print("❌ Webcam access error.")
        return

    cv2.namedWindow('Face Recognition')
    cv2.setMouseCallback('Face Recognition', handle_click)

    recognized_names = set()
    confidence_threshold = 50

    while True:
        ret, frame = video_capture.read()
        if not ret:
            print("❌ Frame read error.")
            break

        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        for face_encoding, (top, right, bottom, left) in zip(face_encodings, face_locations):
            top *= 4; right *= 4; bottom *= 4; left *= 4
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.6)
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            name = "Unknown"
            confidence = 0
            if face_distances.any():
                best_match_index = np.argmin(face_distances)
                confidence = (1 - face_distances[best_match_index]) * 100
                if matches[best_match_index] and confidence > confidence_threshold:
                    name = known_face_names[best_match_index]
            if name != "Unknown":
                recognized_names.add(name)
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, f"{name} ({confidence:.1f}%)", (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)

        # Draw button
        x1, y1, x2, y2 = button_coords
        cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 255, 255), -1)
        cv2.putText(frame, button_text, (x1 + 10, y1 + 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)

        if clicked and recognized_names:
            logged = log_attendance(recognized_names, classroom_id)
            clicked = False
            recognized_names.clear()
            for i, name in enumerate(logged):
                cv2.putText(frame, f"✅ {name} logged!", (10, 80 + i * 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.imshow('Face Recognition', frame)
            cv2.waitKey(1000)

        cv2.imshow('Face Recognition', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            if recognized_names:
                log_attendance(recognized_names, classroom_id)
            break

    video_capture.release()
    cv2.destroyAllWindows()
    print("✅ Attendance session complete.")

if __name__ == "__main__":
    recognize_faces()
