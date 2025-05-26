from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from classes.models import Class
from django.db.models.signals import post_save
from django.dispatch import receiver

class CustomUser(AbstractUser):
    is_teacher = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)

class StudentProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='student_profile')
    profile_image = models.ImageField(upload_to='student_profiles/', blank=True, null=True)
    classes = models.ManyToManyField(Class, related_name='students', blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_student_profile(sender, instance, created, **kwargs):
    if created and instance.is_student:
        StudentProfile.objects.create(user=instance)