# Generated by Django 5.2.1 on 2025-05-17 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_studentprofile_user'),
        ('classroom', '0003_alter_classroom_code_alter_classroom_day_of_week_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='classroom',
            name='students',
            field=models.ManyToManyField(blank=True, related_name='enrolled_classes', to='accounts.studentprofile'),
        ),
    ]
