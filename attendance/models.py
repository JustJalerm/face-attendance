from django.db import models
from accounts.models import StudentProfile
from classroom.models import Classroom

class AttendanceRecord(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=[('Present', 'Present')])

    def __str__(self):
        return f"{self.student.user.username} - {self.classroom.name} - {self.timestamp}"
