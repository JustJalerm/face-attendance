from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status
from classroom.models import Classroom
from attendance.models import AttendanceRecord
from accounts.models import StudentProfile
from .serializers import (
    ClassroomSerializer,
    AttendanceRecordSerializer,
    StudentProfileSerializer
)
from django.contrib.auth.decorators import login_required
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication

class ClassroomListAPI(APIView):
    def get(self, request):
        classrooms = Classroom.objects.all()
        serializer = ClassroomSerializer(classrooms, many=True)
        return Response(serializer.data)

class MyClassesAPI(APIView):
    def get(self, request):
        if request.user.is_student:
            profile = request.user.student_profile
            classrooms = profile.joined_classes.all()
            serializer = ClassroomSerializer(classrooms, many=True)
            return Response(serializer.data)
        return Response({"error": "Unauthorized"}, status=401)

class JoinClassAPI(APIView):
    def post(self, request):
        class_code = request.data.get("class_code", "").strip()
        try:
            classroom = Classroom.objects.get(code=class_code)
            profile = request.user.student_profile
            profile.joined_classes.add(classroom)
            return Response({"message": "Joined class successfully."})
        except Classroom.DoesNotExist:
            return Response({"error": "Class not found."}, status=404)

class AttendanceRecordsAPI(APIView):
    def get(self, request):
        if request.user.is_student:
            records = AttendanceRecord.objects.filter(student=request.user.student_profile)
        elif request.user.is_teacher:
            records = AttendanceRecord.objects.filter(classroom__teacher=request.user)
        else:
            return Response({"error": "Unauthorized"}, status=401)
        serializer = AttendanceRecordSerializer(records, many=True)
        return Response(serializer.data)

class SubmitAttendanceAPI(APIView):
    def post(self, request):
        # Example logic
        return Response({"message": "Attendance submitted (dummy)."}, status=200)

class StudentProfileViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = StudentProfile.objects.all()
    serializer_class = StudentProfileSerializer
    permission_classes = [IsAuthenticated]

class ClassroomViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Classroom.objects.all()
    serializer_class = ClassroomSerializer
    permission_classes = [IsAuthenticated]

class AttendanceRecordViewSet(viewsets.ModelViewSet):
    queryset = AttendanceRecord.objects.all()
    serializer_class = AttendanceRecordSerializer
    permission_classes = [IsAuthenticated]

