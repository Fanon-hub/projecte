from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models

class CustomUser(AbstractUser):
    # Custom user fields
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    # Add related_name to avoid conflicts with default User model
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',  # Set a custom related name
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_permissions',  # Set a custom related name
        blank=True
    )
# Model to extend the default User model (UserProfile)
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Link to default User
    bio = models.TextField(blank=True, null=True)  # Short biography
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)  # Profile picture

    def _str_(self):
        return f'{self.user.username} Profile'

# Model for Courses
class Course(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    duration = models.PositiveIntegerField(help_text='Duration in hours', validators=[MinValueValidator(1)])  # Minimum duration of 1 hour
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def _str_(self):
        return self.title

# Model for Course Enrollment
class Enrollment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to User
    course = models.ForeignKey(Course, on_delete=models.CASCADE)  # Link to Course
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'course')  # Ensure one user can only enroll in a course once

    def _str_(self):
        return f'{self.user.username} enrolled in {self.course.title}'

# Model to represent a lesson within a course
class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')  # Link lesson to a course
    title = models.CharField(max_length=200)  # Title of the lesson
    content = models.TextField()  # Main content for the lesson (e.g., text, explanations)
    video_url = models.URLField(blank=True, null=True)  # URL for a video (optional)
    order = models.PositiveIntegerField(default=1, help_text="Order of the lesson in the course")  # Order of lessons within a course
    created_at = models.DateTimeField(auto_now_add=True)  # When the lesson was created
    updated_at = models.DateTimeField(auto_now=True)  # When the lesson was last updated

    class Meta:
        ordering = ['order']  # Ensure lessons are ordered correctly within a course by their 'order' field

    def _str_(self):
        return f"Lesson: {self.title} in {self.course.title}"

    def get_video(self):
        return self.video_url if self.video_url else None