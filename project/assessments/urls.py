from django.urls import path
from . import views

urlpatterns = [
    # URL for viewing the list of assessments
    path('assessments/', views.assessment_list, name='assessment_list'),

    # URL for viewing a specific assessment's details
    path('assessments/<int:id>/', views.assessment_detail, name='assessment_detail'),
    path('create/', views.assessment_create, name='assessment_create'),  # Create a new assessment
    path('<int:id>/edit/', views.assessment_edit, name='assessment_edit'),  # Update an assessment
    path('<int:id>/delete/', views.assessment_delete, name='assessment_delete'),  # Delete an assessment
    path('assessments/<int:id>/take/', views.take_assessment, name='take_assessment'),
    # URL for submitting the assessment answers
    path('assessments/<int:id>/submit/', views.submit_assessment, name='submit_assessment'),

    # URL for viewing the results of a submitted assessment
    path('assessments/<int:id>/result/', views.assessment_result, name='assessment_result'),

]