from django.urls import path
from . import views

urlpatterns = [
    path('my-classes/', views.list_classrooms, name='list_classrooms'),
    path('edit/<int:classroom_id>/', views.edit_classroom, name='edit_classroom'),
    path('delete/<int:classroom_id>/', views.delete_classroom, name='delete_classroom'),
    path('<int:classroom_id>/students/', views.view_students, name='view_students'),
    path('<int:classroom_id>/take-attendance/', views.take_attendance, name='take_attendance'),
    
]
