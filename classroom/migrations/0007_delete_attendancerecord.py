# Generated by Django 5.2.1 on 2025-05-27 19:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('classroom', '0006_attendancerecord'),
    ]

    operations = [
        migrations.DeleteModel(
            name='AttendanceRecord',
        ),
    ]
