from django.contrib import admin

# Register your models here.

from .models import *


@admin.register(Questions)
class QuestionsAdmin (admin.ModelAdmin):
    list_display = ('question', 'slug', 'author', 'category', 'time', 'upvote', 'anonymous')
    search_fields = ('question','author',)

@admin.register(QuestionCategory)
class QuestionCategoryAdmin (admin.ModelAdmin):
    list_display = ('category',)
    search_fields = ('category',)


@admin.register(Answers)
class AnswersAdmin (admin.ModelAdmin):
    list_display = ('question', 'answer', 'author', 'time', 'upvote', 'anonymous')
    search_fields = ('question', 'answer', 'author',)


