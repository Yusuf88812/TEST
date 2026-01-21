from django.contrib import admin
from modeltranslation.admin import TranslationAdmin, TranslationTabularInline, TranslationStackedInline
from .models import Subject, Module, Question, Choice, TestAttempt, TestAnswer

class ChoiceInline(TranslationTabularInline):
    model = Choice
    extra = 4

class QuestionAdmin(TranslationAdmin):
    inlines = [ChoiceInline]
    list_display = ('text', 'module', 'marks')
    list_filter = ('module__subject', 'module')
    
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }

class ModuleInline(TranslationStackedInline):
    model = Module
    extra = 1

class SubjectAdmin(TranslationAdmin):
    inlines = [ModuleInline]
    prepopulated_fields = {'slug': ('name',)}
    
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }

class ModuleAdmin(TranslationAdmin):
    list_display = ('name', 'subject', 'duration')
    list_filter = ('subject',)
    
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }

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
admin.site.register(Module, ModuleAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(TestAttempt, TestAttemptAdmin)
