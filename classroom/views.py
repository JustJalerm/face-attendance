from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Classroom
from .forms import ClassroomForm
import random
import string
import subprocess
import sys

def generate_random_code(length=6):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

def get_unique_code():
    while True:
        code = generate_random_code()
        if not Classroom.objects.filter(code=code).exists():
            return code

@login_required
def list_classrooms(request):
    classrooms = Classroom.objects.filter(teacher=request.user)

    if request.method == 'POST':
        form = ClassroomForm(request.POST)
        if form.is_valid():
            classroom = form.save(commit=False)
            classroom.teacher = request.user
            classroom.save()
            messages.success(request, f"✅ Class '{classroom.name}' created!")
            return redirect('list_classrooms')
    else:
        # Pre-generate a unique code and show it in the form
        form = ClassroomForm(initial={'code': get_unique_code()})

    return render(request, 'classroom/list_classrooms.html', {
        'classrooms': classrooms,
        'form': form,
    })

@login_required
def delete_classroom(request, classroom_id):
    classroom = get_object_or_404(Classroom, id=classroom_id, teacher=request.user)
    classroom.delete()
    return redirect('list_classrooms')

@login_required
def edit_classroom(request, classroom_id):
    classroom = get_object_or_404(Classroom, id=classroom_id, teacher=request.user)
    if request.method == 'POST':
        form = ClassroomForm(request.POST, instance=classroom)
        if form.is_valid():
            form.save()
            return redirect('list_classrooms')
    else:
        form = ClassroomForm(instance=classroom)
    return render(request, 'classroom/edit_classroom.html', {'form': form})

@login_required
def join_class(request):
    if request.method == 'POST':
        class_code = request.POST.get('class_code', '').strip()
        try:
            classroom = Classroom.objects.get(code=class_code)
        except Classroom.DoesNotExist:
            messages.error(request, "Invalid class code.")
            return redirect('student_dashboard')

        student_profile = request.user.student_profile

        if classroom in student_profile.joined_classes.all():
            messages.info(request, "You're already in this class.")
        else:
            student_profile.joined_classes.add(classroom)
            messages.success(request, f"You've successfully joined {classroom.name}!")

    return redirect('student_dashboard')

@login_required
def view_students(request, classroom_id):
    classroom = get_object_or_404(Classroom, id=classroom_id, teacher=request.user)
    students = classroom.students.all()
    return render(request, 'classroom/view_students.html', {
        'classroom': classroom,
        'students': students,
    })

@login_required
def take_attendance(request, classroom_id):
    classroom = get_object_or_404(Classroom, id=classroom_id, teacher=request.user)

    result = subprocess.run(
        [sys.executable, 'recognition/face_attendance.py', str(classroom_id)],
        capture_output=True,
        text=True
    )

    print("STDOUT:\n", result.stdout)
    print("STDERR:\n", result.stderr)

    messages.success(request, "✅ Attendance script executed.")
    return redirect('list_classrooms')
