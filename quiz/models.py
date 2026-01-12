from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.contrib.auth.models import User

class Subject(models.Model):
    name = models.CharField(max_length=100, verbose_name="Fan nomi")
    description = models.TextField(blank=True, verbose_name="Tavsif")
    image = models.ImageField(upload_to='subjects/', blank=True, null=True, verbose_name="Rasm")
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        verbose_name = "Fan"
        verbose_name_plural = "Fanlar"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Module(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='modules', verbose_name="Fan")
    name = models.CharField(max_length=100, verbose_name="Modul nomi")
    description = models.TextField(blank=True, verbose_name="Tavsif")
    order = models.PositiveIntegerField(default=0, verbose_name="Tartib raqami")
    duration = models.PositiveIntegerField(default=30, help_text="Daqiqalarda kiriting", verbose_name="Davomiyligi (daqiqa)")

    class Meta:
        ordering = ['order']
        verbose_name = "Modul"
        verbose_name_plural = "Modullar"

    def __str__(self):
        return f"{self.subject.name} - {self.name}"

class Question(models.Model):
    QUESTION_TYPES = (
        ('MCQ', 'Ko\'p tanlovli (Test)'),
        ('CODE', 'Kod yozish (Amaliy)'),
    )
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='questions', verbose_name="Modul")
    text = models.TextField(verbose_name="Savol matni")
    question_type = models.CharField(max_length=4, choices=QUESTION_TYPES, default='MCQ', verbose_name="Savol turi")
    image = models.ImageField(upload_to='questions/', blank=True, null=True, verbose_name="Rasm (ixtiyoriy)")
    marks = models.PositiveIntegerField(default=1, verbose_name="Ball")

    class Meta:
        verbose_name = "Savol"
        verbose_name_plural = "Savollar"

    def __str__(self):
        return f"{self.module.name} - {self.text[:50]}"

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices', verbose_name="Savol")
    text = models.CharField(max_length=255, verbose_name="Variant matni")
    is_correct = models.BooleanField(default=False, verbose_name="To'g'ri javobmi?")

    class Meta:
        verbose_name = "Variant"
        verbose_name_plural = "Variantlar"

    def __str__(self):
        return self.text

class TestAttempt(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='attempts', verbose_name="Modul")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='attempts', verbose_name="Foydalanuvchi")
    score = models.IntegerField(default=0, verbose_name="Ball")
    total_questions = models.IntegerField(default=0, verbose_name="Jami savollar")
    correct_answers = models.IntegerField(default=0, verbose_name="To'g'ri javoblar")
    start_time = models.DateTimeField(default=timezone.now, verbose_name="Boshlangan vaqt")
    completed = models.BooleanField(default=False, verbose_name="Tugatilgan")
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name="Tugatilgan vaqt")
    date_taken = models.DateTimeField(auto_now=True, verbose_name="Topshirilgan sana")

    class Meta:
        verbose_name = "Test urinishi"
        verbose_name_plural = "Test urinishlari"

    def __str__(self):
        return f"{self.user.username} - {self.module.name}"

class TestAnswer(models.Model):
    attempt = models.ForeignKey(TestAttempt, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_choice = models.ForeignKey(Choice, on_delete=models.CASCADE, null=True, blank=True)
    code_answer = models.TextField(blank=True, null=True)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"Answer for {self.attempt}"

class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Foydalanuvchi")
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)], verbose_name="Baholash")
    comment = models.TextField(verbose_name="Izoh")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan vaqt")

    class Meta:
        verbose_name = "Fikr-mulohaza"
        verbose_name_plural = "Fikr-mulohazalar"

    def __str__(self):
        return f"{self.user.username} - {self.rating}"
