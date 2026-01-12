from django.contrib import admin
from .models import Subject, Module, Question, Choice, TestAttempt, TestAnswer

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 4

class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    list_display = ('text', 'module', 'marks')
    list_filter = ('module__subject', 'module')

class ModuleInline(admin.StackedInline):
    model = Module
    extra = 1

class SubjectAdmin(admin.ModelAdmin):
    inlines = [ModuleInline]
    prepopulated_fields = {'slug': ('name',)}

class TestAnswerInline(admin.TabularInline):
    model = TestAnswer
    readonly_fields = ('question', 'selected_choice', 'is_correct')
    can_delete = False
    extra = 0

class TestAttemptAdmin(admin.ModelAdmin):
    list_display = ('user', 'module', 'score', 'date_taken')
    list_filter = ('module__subject', 'module', 'date_taken')
    inlines = [TestAnswerInline]
    readonly_fields = ('score', 'total_questions', 'correct_answers', 'date_taken')

admin.site.register(Subject, SubjectAdmin)
admin.site.register(Module)
admin.site.register(Question, QuestionAdmin)
admin.site.register(TestAttempt, TestAttemptAdmin)
