from django.shortcuts import render, get_object_or_404, redirect
from .models import Assessment, AssessmentResult
from django.contrib.auth.decorators import login_required

# Create your views here.

# Read all assessments
def assessment_list(request):
    assessments = Assessment.objects.all()
    return render(request, 'assessment/assessment_list.html', {'assessments': assessments})

# Create a new assessment
def assessment_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        course_id = request.POST.get('course_id')
        max_score = request.POST.get('max_score')
        Assessment.objects.create(
            title=title,
            description=description,
            course_id=course_id,
            max_score=max_score
        )
        return redirect('assessment_list')
    return render(request, 'assessment/assessment_form.html')

# Read a single assessment
def assessment_detail(request, id):
    assessment = get_object_or_404(Assessment, id=id)
    return render(request, 'assessment/assessment_detail.html', {'assessment': assessment})

# Update an assessment
def assessment_edit(request, id):
    assessment = get_object_or_404(Assessment, id=id)
    if request.method == 'POST':
        assessment.title = request.POST.get('title')
        assessment.description = request.POST.get('description')
        assessment.course_id = request.POST.get('course_id')
        assessment.max_score = request.POST.get('max_score')
        assessment.save()
        return redirect('assessment_list')
    return render(request, 'assessment/assessment_form.html', {'assessment': assessment})

# Delete an assessment
def assessment_delete(request, id):
    assessment = get_object_or_404(Assessment, id=id)
    if request.method == 'POST':
        assessment.delete()
        return redirect('assessment_list')
    return render(request, 'assessment/assessment_confirm_delete.html', {'assessment': assessment})

@login_required
def take_assessment(request, assessment_id):
    assessment = get_object_or_404(Assessment, id=assessment_id)
    
    if request.method == 'POST':
            total_score = 0
            for question_id, user_answer in request.POST.items():
                if question_id.startswith("question_"):
                    question_id = int(question_id.split("_")
[1])
                    total_score += 1
            AssessmentResult.objects.create(
                
                user=request.user,
                assessment=assessment,
                score=total_score
            )
            return redirect('assessment_result', assessment_id=assessment.id)
    
    questions = []
    return render(request, 'assessment/take_assessment.html',
                      {'assessment': assessment, 'questions': questions})

@login_required
def submit_assessment(request, assessment_id):
    assessment = get_object_or_404(Assessment, id=assessment_id)

    if request.method == 'POST':
        total_score = 0

        # Process user answers (example logic: adjust based on your question model)
        for question_id, user_answer in request.POST.items():
            if question_id.startswith("question_"):
                question_id = int(question_id.split("_")[1])
                # Add your scoring logic here
                # Example: Increment the total score if the answer is correct
                # Assuming a related Question and Option model for assessment
                total_score += 1  # Increment for correct answers

        # Save the result
        result, created = AssessmentResult.objects.update_or_create(
            user=request.user,
            assessment=assessment,
            defaults={'score': total_score}
        )
        return redirect('assessment_result', assessment_id=assessment.id)

    return render(request, 'assessment/submit_assessment.html', {'assessment': assessment})

@login_required
def submit_assessment_result(request, assessment_id):
    assessment = get_object_or_404(Assessment, id=assessment_id)

    if request.method == 'POST':
        score = int(request.POST.get('score'))
        # Ensure the score does not exceed max_score
        if score > assessment.max_score:
            score = assessment.max_score

        # Save or update the result
        result, created = AssessmentResult.objects.update_or_create(
            user=request.user,
            assessment=assessment,
            defaults={'score': score}
        )
        return redirect('assessment_result', assessment_id=assessment.id)

    return render(request, 'assessment/submit_assessment.html', {'assessment': assessment})


@login_required
def assessment_result(request, assessment_id):
    assessment = get_object_or_404(Assessment, id=assessment_id)
    result = AssessmentResult.objects.filter(user=request.user, assessment=assessment).first()

    return render(request, 'assessment/assessment_result.html', {
        'assessment': assessment,
        'result': result
    })