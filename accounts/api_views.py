# accounts/views_api.py
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import CustomUser, StudentProfile
from classroom.models import Classroom
from attendance.models import AttendanceRecord
from .serializers import (
    UserSerializer, StudentProfileSerializer, 
    ClassroomSerializer, AttendanceRecordSerializer
)
from django.shortcuts import get_object_or_404

class ClassroomListAPI(generics.ListAPIView):
    queryset = Classroom.objects.all()
    serializer_class = ClassroomSerializer
    permission_classes = [permissions.IsAuthenticated]

class MyClassesAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        if request.user.is_student:
            profile = request.user.student_profile
            classrooms = profile.joined_classes.all()
            serializer = ClassroomSerializer(classrooms, many=True)
            return Response(serializer.data)
        return Response({"detail": "Not a student"}, status=403)

class JoinClassAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        code = request.data.get("code")
        classroom = get_object_or_404(Classroom, code=code)
        student_profile = request.user.student_profile
        student_profile.joined_classes.add(classroom)
        return Response({"detail": "Joined successfully!"})

class AttendanceRecordsAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        if request.user.is_teacher:
            records = AttendanceRecord.objects.filter(classroom__teacher=request.user)
        elif request.user.is_student:
            records = AttendanceRecord.objects.filter(student=request.user.student_profile)
        else:
            return Response({"detail": "Access denied"}, status=403)
        serializer = AttendanceRecordSerializer(records, many=True)
        return Response(serializer.data)

class SubmitAttendanceAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        student_id = request.data.get("student_id")
        classroom_id = request.data.get("classroom_id")
        status = request.data.get("status")  # "P", "A", "L"
        student = get_object_or_404(StudentProfile, id=student_id)
        classroom = get_object_or_404(Classroom, id=classroom_id)
        record = AttendanceRecord.objects.create(
            student=student,
            classroom=classroom,
            status=status
        )
        return Response({"detail": "Attendance recorded", "id": record.id})
