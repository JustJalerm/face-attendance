from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, StudentProfileForm, UserForm
from .models import CustomUser, StudentProfile
from classroom.models import Classroom
from attendance.models import AttendanceRecord



def home_redirect(request):
    return redirect('login')


def redirect_based_on_role(request):
    user = request.user
    if user.is_authenticated and user.is_teacher:
        return redirect('teacher_dashboard')
    elif user.is_authenticated and user.is_student:
        return redirect('student_dashboard')
    return redirect('login')


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        role = request.POST.get('role')

        if form.is_valid():
            user = form.save(commit=False)

            # Set user role
            if role == 'teacher':
                user.is_teacher = True
            elif role == 'student':
                user.is_student = True

            user.save()

            # Create student profile if student
            if user.is_student:
                student_profile, created = StudentProfile.objects.get_or_create(user=user)
                if 'photo' in request.FILES:
                    student_profile.photo = request.FILES['photo']
                    student_profile.save()

            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect_based_on_role(user)

        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = CustomUserCreationForm()

    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect_based_on_role(request.user)

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect_based_on_role(request)
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'accounts/login.html')


@login_required
def teacher_dashboard(request):
    if not request.user.is_teacher:
        return redirect('student_dashboard')
    return render(request, 'accounts/teacher_dashboard.html')


@login_required
def student_dashboard(request):
    if not request.user.is_student:
        return redirect('teacher_dashboard')
    return render(request, 'accounts/student_dashboard.html')


@login_required
def join_class(request):
    if request.method == 'POST':
        class_code = request.POST.get('class_code', '').strip()
        try:
            classroom = Classroom.objects.get(code=class_code)
        except Classroom.DoesNotExist:
            messages.error(request, "Invalid class code.")
            return redirect('student_dashboard')

        try:
            student_profile = request.user.student_profile
        except StudentProfile.DoesNotExist:
            messages.error(request, "Student profile not found.")
            return redirect('student_dashboard')

        if classroom in student_profile.joined_classes.all():
            messages.info(request, "You're already in this class.")
        else:
            student_profile.joined_classes.add(classroom)
            messages.success(request, f"You've successfully joined {classroom.name}!")

    return redirect('student_dashboard')


@login_required
def my_classes(request):
    if hasattr(request.user, 'student_profile'):
        classrooms = request.user.student_profile.joined_classes.all()
    else:
        classrooms = []
    return render(request, 'accounts/my_classes.html', {'classrooms': classrooms})


@login_required
def attendance_report(request):
    return render(request, 'accounts/attendance_report.html')

@login_required
def student_profile(request):
    if not request.user.is_student:
        return redirect('student_dashboard')

    user_form = UserForm(instance=request.user)
    profile_form = StudentProfileForm(instance=request.user.student_profile)

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = StudentProfileForm(request.POST, request.FILES, instance=request.user.student_profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('student_profile')

    return render(request, 'accounts/student_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

@login_required
def attendance_report(request):
    if request.user.is_student:
        records = AttendanceRecord.objects.filter(
            student=request.user.student_profile
        ).order_by('-date')
    elif request.user.is_teacher:
        records = AttendanceRecord.objects.filter(
            classroom__teacher=request.user
        ).order_by('-date')
    else:
        records = []

    return render(request, 'accounts/attendance_report.html', {'records': records})

