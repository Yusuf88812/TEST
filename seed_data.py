import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from quiz.models import Subject, Module, Question, Choice

def seed():
    print("Eski ma'lumotlar tozalanmoqda...")
    Subject.objects.all().delete()
    
    # --- PYTHON ---
    python = Subject.objects.create(name="Python Dasturlash", description="AI, Backend va ma'lumotlar tahlili uchun eng mashhur til.")
    
    # Modul 1: Asoslar
    mod_py_basic = Module.objects.create(subject=python, name="Python Asoslari", order=1, description="O'zgaruvchilar, turlar va operatorlar.", duration=15)
    
    q1 = Question.objects.create(module=mod_py_basic, text="Python'da `print(2 ** 3)` natijasi nima?", marks=5)
    Choice.objects.create(question=q1, text="6", is_correct=False)
    Choice.objects.create(question=q1, text="8", is_correct=True)
    Choice.objects.create(question=q1, text="9", is_correct=False)
    
    q2 = Question.objects.create(module=mod_py_basic, text="Funksiyani aniqlash uchun qaysi kalit so'z ishlatiladi?", marks=5)
    Choice.objects.create(question=q2, text="func", is_correct=False)
    Choice.objects.create(question=q2, text="def", is_correct=True)
    Choice.objects.create(question=q2, text="function", is_correct=False)

    q3 = Question.objects.create(module=mod_py_basic, text="Qaysi biri Python'da izoh hisoblanadi?", marks=5)
    Choice.objects.create(question=q3, text="// bu izoh", is_correct=False)
    Choice.objects.create(question=q3, text="# bu izoh", is_correct=True)
    Choice.objects.create(question=q3, text="<!-- bu izoh -->", is_correct=False)
    
    # Modul 2: OOP
    mod_py_oop = Module.objects.create(subject=python, name="OOP (Obyektga Yo'naltirilgan Dasturlash)", order=2, description="Sinflar, obyektlar va merosxo'rlik.", duration=20)
    q_oop1 = Question.objects.create(module=mod_py_oop, text="Sinfdagi konstruktor metod qanday nomlanadi?", marks=10)
    Choice.objects.create(question=q_oop1, text="__init__", is_correct=True)
    Choice.objects.create(question=q_oop1, text="constructor", is_correct=False)
    Choice.objects.create(question=q_oop1, text="__start__", is_correct=False)

    # --- DJANGO ---
    django_subj = Subject.objects.create(name="Django Framework", description="Python da mukammal veb saytlar yaratish.")
    
    mod_dj_intro = Module.objects.create(subject=django_subj, name="Django Kirish", order=1, description="Arxitektura va o'rnatish.", duration=15)
    q_dj1 = Question.objects.create(module=mod_dj_intro, text="Django qaysi arxitektura namunasiga asoslangan?", marks=5)
    Choice.objects.create(question=q_dj1, text="MVC (Model-View-Controller)", is_correct=False)
    Choice.objects.create(question=q_dj1, text="MVT (Model-View-Template)", is_correct=True)
    Choice.objects.create(question=q_dj1, text="MVVM (Model-View-ViewModel)", is_correct=False)

    q_dj2 = Question.objects.create(module=mod_dj_intro, text="Yangi Django loyihasi yaratish buyrug'i nima?", marks=5)
    Choice.objects.create(question=q_dj2, text="django-admin startproject [name]", is_correct=True)
    Choice.objects.create(question=q_dj2, text="python manage.py runserver", is_correct=False)
    Choice.objects.create(question=q_dj2, text="pip install django", is_correct=False)

    # --- HTML ---
    html = Subject.objects.create(name="HTML & CSS", description="Veb sahifa tuzilishi va dizayni.")
    mod_html = Module.objects.create(subject=html, name="HTML5 Asoslari", order=1, description="Teglar, atributlar va semantika.", duration=10)
    
    q_html1 = Question.objects.create(module=mod_html, text="Eng katta sarlavha uchun qaysi teg ishlatiladi?", marks=5)
    Choice.objects.create(question=q_html1, text="<h1>", is_correct=True)
    Choice.objects.create(question=q_html1, text="<h6>", is_correct=False)
    Choice.objects.create(question=q_html1, text="<header>", is_correct=False)

    print("Ma'lumotlar bazasi muvaffaqiyatli to'ldirildi!")

if __name__ == '__main__':
    seed()
