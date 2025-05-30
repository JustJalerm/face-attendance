import os
import sys
import django
import face_recognition
import pickle

# ✅ Setup Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "attendance.settings")
django.setup()

# ✅ Safe to import now
from accounts.models import StudentProfile

KNOWN_FACES_PATH = "recognition/known_faces.pkl"

def encode_faces():
    known_encodings = []
    known_names = []
    student_ids = []

    students = StudentProfile.objects.all()
    for student in students:
        if student.profile_image:
            image_path = student.profile_image.path
            print(f"✅ Encoding {student.user.username} from {image_path}")
            try:
                image = face_recognition.load_image_file(image_path)
                encodings = face_recognition.face_encodings(image)
                if encodings:
                    known_encodings.append(encodings[0])
                    known_names.append(student.user.username)
                    student_ids.append(student.id)
                else:
                    print(f"❌ No face found in {image_path}")
            except Exception as e:
                print(f"❌ Error processing {image_path}: {e}")

            with open(KNOWN_FACES_PATH, "wb") as f:
                    pickle.dump({
                "encodings": known_encodings,
                "names": known_names,
                "ids": student_ids
                }, f)
    print(f"✅ Saved {len(known_encodings)} encoded face(s) to {KNOWN_FACES_PATH}")


if __name__ == "__main__":
    encode_faces()
