from django.urls import path, include
from . import views
from django.contrib.auth.views import LogoutView
from .views import request_permission

from .views_api import (
    ClassroomListAPI, MyClassesAPI, JoinClassAPI,
    AttendanceRecordsAPI, SubmitAttendanceAPI,
    StudentProfileViewSet, ClassroomViewSet, AttendanceRecordViewSet
)
from rest_framework.routers import DefaultRouter

# ✅ Set up DRF router
router = DefaultRouter()
router.register(r'profiles', StudentProfileViewSet, basename='profiles')
router.register(r'classrooms', ClassroomViewSet, basename='classrooms')
router.register(r'attendance', AttendanceRecordViewSet, basename='attendance')

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
    path('request-permission/<int:record_id>/', request_permission, name='request_permission'),

    # ✅ DRF API endpoints
    path('api/classrooms/', ClassroomListAPI.as_view(), name='api_classrooms'),
    path('api/my-classes/', MyClassesAPI.as_view(), name='api_my_classes'),
    path('api/join-class/', JoinClassAPI.as_view(), name='api_join_class'),
    path('api/attendance-records/', AttendanceRecordsAPI.as_view(), name='api_attendance_records'),
    path('api/submit-attendance/', SubmitAttendanceAPI.as_view(), name='api_submit_attendance'),
    path('api/', include(router.urls)),

    # ✅ DRF login/logout (Browsable API auth)
    path('api-auth/', include('rest_framework.urls')),
]
