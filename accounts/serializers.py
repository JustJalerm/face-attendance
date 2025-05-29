from rest_framework import serializers
from .models import CustomUser, StudentProfile
from classroom.models import Classroom
from attendance.models import AttendanceRecord

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'is_teacher', 'is_student']

class StudentProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = StudentProfile
        fields = ['id', 'user', 'profile_image']

class ClassroomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classroom
        fields = ['id', 'name', 'code', 'scheduled_time']

class AttendanceRecordSerializer(serializers.ModelSerializer):
    student = StudentProfileSerializer()
    classroom = ClassroomSerializer()
    
    class Meta:
        model = AttendanceRecord
        fields = ['id', 'student', 'classroom', 'status', 'timestamp']
