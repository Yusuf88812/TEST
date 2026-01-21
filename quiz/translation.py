from modeltranslation.translator import register, TranslationOptions
from .models import Subject, Module, Question, Choice

@register(Subject)
class SubjectTranslationOptions(TranslationOptions):
    fields = ('name', 'description')

@register(Module)
class ModuleTranslationOptions(TranslationOptions):
    fields = ('name', 'description')

@register(Question)
class QuestionTranslationOptions(TranslationOptions):
    fields = ('text',)

@register(Choice)
class ChoiceTranslationOptions(TranslationOptions):
    fields = ('text',)
