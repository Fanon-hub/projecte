from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ContactForm
from .models import Course, Enrollment, Lesson
from django.core.mail import send_mail


# Registration View
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


# Profile View
@login_required
def profile(request):
    return render(request, 'users/profile.html')


# Edit Profile View
@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
    return render(request, 'users/edit_profile.html', {'user_form': user_form})

# View to all courses
def course_list(request):
    courses = Course.objects.all()
    return render(request, 'courses/course_list.html', {'courses': courses})
# View to show details of a specific course
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    lessons = Lesson.objects.filter(course=course)  # Get lessons related to this course
    return render(request, 'courses/course_detail.html', {'course': course, 'lessons': lessons})

# View for course enrollment
@login_required
def enroll(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    # Check if the user is already enrolled in the course
    if Enrollment.objects.filter(user=request.user, course=course).exists():
        return render(request, 'courses/enrollment_error.html', {'message': 'You are already enrolled in this course.'})

    # Create an enrollment for the user
    Enrollment.objects.create(user=request.user, course=course)
    return render(request, 'courses/enrollment_success.html', {'course': course})


# View to list all lessons for a specific course
def lesson_list(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    lessons = Lesson.objects.filter(course=course)
    return render(request, 'courses/lesson_list.html', {'course': course, 'lessons': lessons})


# View to show a specific lesson's details
def lesson_detail(request, course_id, lesson_id):
    course = get_object_or_404(Course, id=course_id)
    lesson = get_object_or_404(Lesson, id=lesson_id, course=course)
    return render(request, 'courses/lesson_detail.html', {'course': course, 'lesson': lesson})
def courses(request):

    return render(request, 'courses.html')
def about(request):
    return render(request, 'about.html')
def contact(request):
    return render(request, 'contact.html')

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Process form data (e.g., send an email)
            send_mail(
                f"Contact Inquiry from {form.cleaned_data['name']}",
                form.cleaned_data['message'],
                form.cleaned_data['email'],
                ['support@reskillplatform.com']
            )
            return render(request, 'users/contact.html', {'form': form, 'success': True})
    else:
        form = ContactForm()
    return render(request, 'users/contact.html', {'form': form})
