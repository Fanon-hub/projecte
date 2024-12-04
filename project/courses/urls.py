from django.urls import path
from . import views

urlpatterns = [
    # URL for listing all courses
    path('courses/', views.course_list, name='course_list'), #Read all courses
    path('create/', views.course_create, name='course_create'), #Create a new course
    # URL for viewing a specific course's detail page
    path('courses/<int:id>/', views.course_detail, name='course_detail'), #Read a single course
    path('<int:id>/edit/', views.course_edit, name='course_edit'), #Update a course
    path('<int:id>/delete/', views.course_delete, name='course_delete'), #Delete a course
]