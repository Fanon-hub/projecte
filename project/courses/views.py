from django.shortcuts import render, get_object_or_404, redirect
from .models import Course

# Read all courses
def course_list(request):
    courses = Course.objects.all()
    return render(request, 'courses/course_list.html', {'courses': courses})

# Create a new course
def course_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        Course.objects.create(title=title, description=description)
        return redirect('course_list')
    return render(request, 'courses/course_form.html')

# Read a single course
def course_detail(request, id):
    course = get_object_or_404(Course, id=id)
    return render(request, 'courses/course_detail.html', {'course': course})

# Update a course
def course_edit(request, id):
    course = get_object_or_404(Course, id=id)
    if request.method == 'POST':
        course.title = request.POST.get('title')
        course.description = request.POST.get('description')
        course.save()
        return redirect('course_list')
    return render(request, 'courses/course_form.html', {'course': course})

# Delete a course
def course_delete(request, id):
    course = get_object_or_404(Course, id=id)
    if request.method == 'POST':
        course.delete()
        return redirect('course_list')
    return render(request, 'courses/course_confirm_delete.html', {'course': course})