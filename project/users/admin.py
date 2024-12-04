from django.contrib import admin
from .models import UserProfile, Course, Enrollment, Lesson

# Register models in the admin site
admin.site.register(UserProfile)
admin.site.register(Course)
admin.site.register(Enrollment)
admin.site.register(Lesson)
from django.contrib import admin


