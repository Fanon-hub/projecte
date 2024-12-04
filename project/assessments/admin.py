from django.contrib import admin
from .models import Assessment, AssessmentResult, Question, Option


@admin.register(Assessment)
class AssessmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'max_score', 'created_at', 'updated_at')
    search_fields = ('title', 'course__name')
    list_filter = ('course', 'created_at')
    ordering = ('-created_at',)


@admin.register(AssessmentResult)
class AssessmentResultAdmin(admin.ModelAdmin):
    list_display = ('user', 'assessment', 'score', 'submitted_at')
    search_fields = ('user_username', 'assessment_title')
    list_filter = ('submitted_at',)
    ordering = ('-submitted_at',)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'assessment')
    search_fields = ('text', 'assessment__title')
    list_filter = ('assessment',)


@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ('text', 'question', 'is_correct')
    search_fields = ('text', 'question__text')
    list_filter = ('is_correct',)

class OptionInline(admin.TabularInline):
    model = Option
    extra = 1  # Number of empty forms to display for new options


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1  # Number of empty forms to display for new questions


@admin.register(Assessment)
class AssessmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'max_score', 'created_at', 'updated_at')
    inlines = [QuestionInline]  # Embed questions in the assessment admin
