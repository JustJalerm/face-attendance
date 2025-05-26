from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('', views.home_redirect, name='home_redirect'),
    path('login/', views.login_view, name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.redirect_based_on_role, name='dashboard'),
    path('dashboard/teacher/', views.teacher_dashboard, name='teacher_dashboard'),
    path('dashboard/student/', views.student_dashboard, name='student_dashboard'),
    path('join-class/', views.join_class, name='join_class'),
    path('my-classes/', views.my_classes, name='my_classes'),
    path('attendance-report/', views.attendance_report, name='attendance_report'),
    path('profile/', views.student_profile, name='student_profile'),
]