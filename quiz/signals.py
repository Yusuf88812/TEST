from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.conf import settings
from .models import Subject, Module, Question, Choice

@receiver(pre_save, sender=Subject)
@receiver(pre_save, sender=Module)
@receiver(pre_save, sender=Question)
@receiver(pre_save, sender=Choice)
def auto_fill_translations(sender, instance, **kwargs):
    """
    Automatically fills empty translation fields with content from
    available languages to prevent blank content.
    """
    languages = [lang[0] for lang in settings.LANGUAGES]
    
    # Define which fields to check for each model
    model_fields_map = {
        Subject: ['name', 'description'],
        Module: ['name', 'description'],
        Question: ['text'],
        Choice: ['text'],
    }
    
    fields_to_check = model_fields_map.get(sender, [])
    
    for field_base in fields_to_check:
        # 1. Find a source string from any of the language fields
        source_text = None
        
        # Try finding a non-empty value in order of languages (usually starts with 'uz')
        for lang in languages:
            val = getattr(instance, f'{field_base}_{lang}', None)
            if val:
                source_text = val
                break
        
        # If we still don't have text, check the main field (unlikely to be different but good fallback)
        if not source_text:
            source_text = getattr(instance, field_base, None)
            
        # If we absolutely have no text, skip
        if not source_text:
            continue
            
        # 2. Populate empty fields with the found source text
        for lang in languages:
            field_name = f'{field_base}_{lang}'
            current_val = getattr(instance, field_name, None)
            
            # Check if it's empty (None or "")
            if not current_val:
                setattr(instance, field_name, source_text)
