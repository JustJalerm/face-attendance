from django.db import models
from django.conf import settings
from accounts.models import StudentProfile

class Classroom(models.Model):
    DAY_CHOICES = [
        ('MON', 'Monday'),
        ('TUE', 'Tuesday'),
        ('WED', 'Wednesday'),
        ('THU', 'Thursday'),
        ('FRI', 'Friday'),
        ('SAT', 'Saturday'),
        ('SUN', 'Sunday'),
    ]

    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    description = models.TextField(blank=True)
    day_of_week = models.CharField(max_length=3, choices=DAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    students = models.ManyToManyField(StudentProfile, related_name='joined_classes', blank=True)

    def __str__(self):
        return f"{self.name} ({self.code})"

    def scheduled_time(self):
        return f"{self.get_day_of_week_display()} {self.start_time.strftime('%H:%M')} - {self.end_time.strftime('%H:%M')}"
