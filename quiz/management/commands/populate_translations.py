from django.core.management.base import BaseCommand
from django.conf import settings
from quiz.models import Subject, Module, Question, Choice
from django.db import transaction

class Command(BaseCommand):
    help = 'Populates missing translations for all models'

    def handle(self, *args, **options):
        self.stdout.write('Starting translation population...')
        
        languages = [lang[0] for lang in settings.LANGUAGES]
        
        with transaction.atomic():
            # Subjects
            self.stdout.write('Processing Subjects...')
            for obj in Subject.objects.all():
                source_name = getattr(obj, 'name_uz', None) or getattr(obj, 'name', None)
                source_desc = getattr(obj, 'description_uz', None) or getattr(obj, 'description', None)
                
                changed = False
                for lang in languages:
                    # Name
                    field_name = f'name_{lang}'
                    if not getattr(obj, field_name) and source_name:
                        setattr(obj, field_name, source_name)
                        changed = True
                    # Description
                    field_desc = f'description_{lang}'
                    if not getattr(obj, field_desc) and source_desc:
                        setattr(obj, field_desc, source_desc)
                        changed = True
                if changed:
                    obj.save()
                    
            # Modules
            self.stdout.write('Processing Modules...')
            for obj in Module.objects.all():
                source_name = getattr(obj, 'name_uz', None) or getattr(obj, 'name', None)
                source_desc = getattr(obj, 'description_uz', None) or getattr(obj, 'description', None)

                changed = False
                for lang in languages:
                    field_name = f'name_{lang}'
                    if not getattr(obj, field_name) and source_name:
                        setattr(obj, field_name, source_name)
                        changed = True
                    field_desc = f'description_{lang}'
                    if not getattr(obj, field_desc) and source_desc:
                        setattr(obj, field_desc, source_desc)
                        changed = True
                if changed:
                    obj.save()

            # Questions
            self.stdout.write('Processing Questions...')
            for obj in Question.objects.all():
                # Determine source text (try 'uz' first, then default 'text')
                source_text = getattr(obj, 'text_uz', None) or getattr(obj, 'text', None)
                if not source_text:
                    continue  # Skip if no source text found

                changed = False
                for lang in languages:
                    field_text = f'text_{lang}'
                    if not getattr(obj, field_text):
                        setattr(obj, field_text, source_text)
                        changed = True
                if changed:
                    obj.save()

            # Choices
            self.stdout.write('Processing Choices...')
            for obj in Choice.objects.all():
                source_text = getattr(obj, 'text_uz', None) or getattr(obj, 'text', None)
                if not source_text:
                    continue

                changed = False
                for lang in languages:
                    field_text = f'text_{lang}'
                    if not getattr(obj, field_text):
                        setattr(obj, field_text, source_text)
                        changed = True
                if changed:
                    obj.save()

        self.stdout.write(self.style.SUCCESS('Successfully populated translations!'))
