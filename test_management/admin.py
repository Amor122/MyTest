from django.contrib import admin

from . import models


@admin.register(models.Subject)
class SubjectModelAdmin(admin.ModelAdmin):
    list_display = ('subject_name',)
    fields = ('subject_name',)
    list_per_page = 10
    search_fields = ('subject_name',)


@admin.register(models.Difficulty)
class DifficultyModelAdmin(admin.ModelAdmin):
    list_display = ('difficulty_name',)
    fields = ('difficulty_name',)
    list_per_page = 10
    search_fields = ('difficulty_name',)


@admin.register(models.Test)
class TestModelAdmin(admin.ModelAdmin):
    list_display = ('subject', 'difficulty', 'test_name')
    fields = ('subject', 'difficulty', 'test_name', 'start_time', 'duration')
    list_per_page = 10
    search_fields = ('test_name',)


@admin.register(models.Invigilator)
class InvigilatorModelAdmin(admin.ModelAdmin):
    list_display = ('test', 'test')
    fields = ('test', 'test')
    list_per_page = 10


@admin.register(models.Paper)
class PaperModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'test',)
    fields = ('test',)
    list_per_page = 10


@admin.register(models.PaperQuestion)
class PaperQuestionModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'paper', 'paper_number',)
    fields = ('paper', 'paper_number', 'question', 'score')
    list_per_page = 10


@admin.register(models.PaperAnswer)
class PaperAnswerModelAdmin(admin.ModelAdmin):
    list_display = ('examinee', 'paper_question', 'score_get',)
    fields = ('examinee', 'paper_question', 'my_answer', 'score_get')
    list_per_page = 10
