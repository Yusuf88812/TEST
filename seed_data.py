import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from quiz.models import Subject, Module, Question, Choice

def seed():
    print("Eski ma'lumotlar tozalanmoqda...")
    Subject.objects.all().delete()
    
    # Define Subjects and their difficulty levels with translations
    subjects_data = [
        {
            "name": {"uz": "Python Dasturlash", "ru": "Программирование на Python", "en": "Python Programming"}, 
            "desc": {"uz": "AI, Backend va ma'lumotlar tahlili uchun eng mashhur til.", "ru": "Самый популярный язык для ИИ, бэкенда и анализа данных.", "en": "The most popular language for AI, Backend, and Data Analysis."},
            "code": "py",
            "terms": {
                "basic": [
                    ("print()", {"uz": "Chop etish", "ru": "Вывод на экран", "en": "Print to screen"}), 
                    ("int", {"uz": "Butun son", "ru": "Целое число", "en": "Integer"}), 
                    ("str", {"uz": "Satr", "ru": "Строка", "en": "String"}), 
                    ("bool", {"uz": "Mantiqiy", "ru": "Логический", "en": "Boolean"}), 
                    ("float", {"uz": "Haqiqiy son", "ru": "Вещественное число", "en": "Float"})
                ],
                "medium": [
                    ("list", {"uz": "Ro'yxat", "ru": "Список", "en": "List"}), 
                    ("dict", {"uz": "Lug'at", "ru": "Словарь", "en": "Dictionary"}), 
                    ("tuple", {"uz": "Kortej", "ru": "Кортеж", "en": "Tuple"}), 
                    ("set", {"uz": "To'plam", "ru": "Множество", "en": "Set"}), 
                    ("def", {"uz": "Funksiya", "ru": "Функция", "en": "Function"})
                ],
                "high": [
                    ("class", {"uz": "Sinf", "ru": "Класс", "en": "Class"}), 
                    ("inheritance", {"uz": "Merosxo'rlik", "ru": "Наследование", "en": "Inheritance"}), 
                    ("polymorphism", {"uz": "Polimorfizm", "ru": "Полиморфизм", "en": "Polymorphism"}), 
                    ("lambda", {"uz": "Nomsiz funksiya", "ru": "Лямбда-функция", "en": "Lambda function"}), 
                    ("yield", {"uz": "Generator", "ru": "Генератор", "en": "Generator"})
                ],
                "expert": [
                    ("GIL", {"uz": "Global Interpreter Lock", "ru": "Глобальная блокировка интерпретатора", "en": "Global Interpreter Lock"}), 
                    ("Metaclass", {"uz": "Sinflarni yaratuvchi sinf", "ru": "Метакласс", "en": "Metaclass"}), 
                    ("Decorator", {"uz": "Funksiya bezagi", "ru": "Декоратор", "en": "Decorator"}), 
                    ("Context Manager", {"uz": "with operatori", "ru": "Менеджер контекста", "en": "Context Manager"}), 
                    ("Asyncio", {"uz": "Asinxron dasturlash", "ru": "Асинхронное программирование", "en": "Asyncio"})
                ]
            }
        },
        {
            "name": {"uz": "Django Framework", "ru": "Django Фреймворк", "en": "Django Framework"}, 
            "desc": {"uz": "Python da mukammal veb saytlar yaratish.", "ru": "Создание совершенных веб-сайтов на Python.", "en": "Building perfect websites with Python."},
            "code": "dj",
            "terms": {
                "basic": [
                    ("Model", {"uz": "Ma'lumotlar tuzilmasi", "ru": "Структура данных", "en": "Data structure"}), 
                    ("View", {"uz": "Mantiqiy qism", "ru": "Представление", "en": "View logic"}), 
                    ("Template", {"uz": "Ko'rinish", "ru": "Шаблон", "en": "Template"}), 
                    ("URL", {"uz": "Manzil", "ru": "Адрес", "en": "URL"}), 
                    ("Admin", {"uz": "Boshqaruv paneli", "ru": "Панель администратора", "en": "Admin panel"})
                ],
                "medium": [
                    ("ORM", {"uz": "Object-Relational Mapping", "ru": "ORM", "en": "ORM"}), 
                    ("QuerySet", {"uz": "Ma'lumotlar so'rovi", "ru": "Запрос данных", "en": "QuerySet"}), 
                    ("Context", {"uz": "Shablon ma'lumotlari", "ru": "Контекст", "en": "Context"}), 
                    ("Form", {"uz": "Ma'lumot kiritish", "ru": "Форма", "en": "Form"}), 
                    ("Migration", {"uz": "DB o'zgarishlari", "ru": "Миграция", "en": "Migration"})
                ],
                "high": [
                    ("Middleware", {"uz": "Oraliq dastur", "ru": "Промежуточное ПО", "en": "Middleware"}), 
                    ("Signal", {"uz": "Hodisalar", "ru": "Сигналы", "en": "Signal"}), 
                    ("Mixin", {"uz": "Qo'shimcha funksional", "ru": "Миксин", "en": "Mixin"}), 
                    ("CBV", {"uz": "Class Based Views", "ru": "Классовые представления", "en": "CBV"}), 
                    ("Serializer", {"uz": "JSON o'giruvchi", "ru": "Сериализатор", "en": "Serializer"})
                ],
                "expert": [
                    ("Channels", {"uz": "WebSockets", "ru": "Веб-сокеты", "en": "WebSockets"}), 
                    ("Celery", {"uz": "Orqa fon vazifalari", "ru": "Фоновые задачи", "en": "Background tasks"}), 
                    ("Cache", {"uz": "Keshlash", "ru": "Кэширование", "en": "Caching"}), 
                    ("Optimizing", {"uz": "Tezlashtirish", "ru": "Оптимизация", "en": "Optimizing"}), 
                    ("Security", {"uz": "Xavfsizlik", "ru": "Безопасность", "en": "Security"})
                ]
            }
        },
        # Add more logic for other subjects similarly or keep basic placeholders if needed
        # For brevity, implementing full stack for the first two, and simple for others
    ]

    difficulties = [
        ({"uz": "Boshlang'ich", "ru": "Начальный", "en": "Basic"}, 1, 15, "basic"),
        ({"uz": "O'rta", "ru": "Средний", "en": "Intermediate"}, 2, 20, "medium"),
        ({"uz": "Yuqori", "ru": "Высокий", "en": "Advanced"}, 3, 25, "high"),
        ({"uz": "Ekspert", "ru": "Эксперт", "en": "Expert"}, 4, 30, "expert")
    ]

    total_questions_created = 0

    for subj_data in subjects_data:
        subject = Subject.objects.create(
            name=subj_data["name"]["uz"],
            name_uz=subj_data["name"]["uz"],
            name_ru=subj_data["name"]["ru"],
            name_en=subj_data["name"]["en"],
            description=subj_data["desc"]["uz"],
            description_uz=subj_data["desc"]["uz"],
            description_ru=subj_data["desc"]["ru"],
            description_en=subj_data["desc"]["en"]
        )
        print(f"Added Subject: {subject.name}")

        for diff_names, diff_order, diff_duration, term_key in difficulties:
            if term_key not in subj_data["terms"]:
                 continue # Skip if terms not defined
                 
            module = Module.objects.create(
                subject=subject,
                name=f"{diff_names['uz']} daraja",
                name_uz=f"{diff_names['uz']} daraja",
                name_ru=f"{diff_names['ru']} уровень",
                name_en=f"{diff_names['en']} level",
                order=diff_order,
                description=f"{subj_data['name']['uz']} bo'yicha {diff_names['uz'].lower()} bilimlar.",
                description_uz=f"{subj_data['name']['uz']} bo'yicha {diff_names['uz'].lower()} bilimlar.",
                description_ru=f"Знания по {subj_data['name']['ru']} ({diff_names['ru']}).",
                description_en=f"{diff_names['en']} knowledge in {subj_data['name']['en']}.",
                duration=diff_duration
            )
            
            terms = subj_data["terms"][term_key]
            
            for i in range(1, 51):
                term_name, term_descs = terms[i % len(terms)]
                
                # Q Type 1: Definition
                if i % 2 == 0:
                    q_text_uz = f"{subj_data['name']['uz']} ({diff_names['uz']}): '{term_name}' atamasi nimani anglatadi? (Savol {i})"
                    q_text_ru = f"{subj_data['name']['ru']} ({diff_names['ru']}): Что означает термин '{term_name}'? (Вопрос {i})"
                    q_text_en = f"{subj_data['name']['en']} ({diff_names['en']}): What does '{term_name}' mean? (Question {i})"
                    
                    correct_text = term_descs
                    
                    # Wrong answers (just taking others)
                    w1 = terms[(i + 1) % len(terms)][1]
                    w2 = terms[(i + 2) % len(terms)][1]
                    w3 = terms[(i + 3) % len(terms)][1]
                    
                else:
                    q_text_uz = f"{subj_data['name']['uz']} ({diff_names['uz']}): {term_descs['uz']} uchun qaysi atama ishlatiladi? (Savol {i})"
                    q_text_ru = f"{subj_data['name']['ru']} ({diff_names['ru']}): Какой термин используется для: {term_descs['ru']}? (Вопрос {i})"
                    q_text_en = f"{subj_data['name']['en']} ({diff_names['en']}): Which term is used for: {term_descs['en']}? (Question {i})"

                    correct_text = {"uz": term_name, "ru": term_name, "en": term_name}
                    
                    # Wrong answers (names)
                    w1 = {"uz": terms[(i + 1) % len(terms)][0], "ru": terms[(i + 1) % len(terms)][0], "en": terms[(i + 1) % len(terms)][0]}
                    w2 = {"uz": terms[(i + 2) % len(terms)][0], "ru": terms[(i + 2) % len(terms)][0], "en": terms[(i + 2) % len(terms)][0]}
                    w3 = {"uz": terms[(i + 3) % len(terms)][0], "ru": terms[(i + 3) % len(terms)][0], "en": terms[(i + 3) % len(terms)][0]}

                q = Question.objects.create(
                    module=module,
                    text=q_text_uz,
                    text_uz=q_text_uz,
                    text_ru=q_text_ru,
                    text_en=q_text_en,
                    marks=5
                )
                
                Choice.objects.create(
                    question=q, 
                    text=correct_text['uz'],
                    text_uz=correct_text['uz'],
                    text_ru=correct_text['ru'],
                    text_en=correct_text['en'],
                    is_correct=True
                )
                Choice.objects.create(
                    question=q, 
                    text=w1['uz'],
                    text_uz=w1['uz'],
                    text_ru=w1['ru'],
                    text_en=w1['en'],
                    is_correct=False
                )
                Choice.objects.create(
                    question=q, 
                    text=w2['uz'],
                    text_uz=w2['uz'],
                    text_ru=w2['ru'],
                    text_en=w2['en'],
                    is_correct=False
                )
                Choice.objects.create(
                    question=q, 
                    text=w3['uz'],
                    text_uz=w3['uz'],
                    text_ru=w3['ru'],
                    text_en=w3['en'],
                    is_correct=False
                )
                
                total_questions_created += 1

    print(f"Jami {total_questions_created} ta savol va ma'lumotlar bazasi (UZ/RU/EN) muvaffaqiyatli yaratildi!")

if __name__ == '__main__':
    seed()
