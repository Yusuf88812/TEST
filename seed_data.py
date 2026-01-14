import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from quiz.models import Subject, Module, Question, Choice

def seed():
    print("Eski ma'lumotlar tozalanmoqda...")
    Subject.objects.all().delete()
    
    # Define Subjects and their difficulty levels
    subjects_data = [
        {
            "name": "Python Dasturlash", 
            "desc": "AI, Backend va ma'lumotlar tahlili uchun eng mashhur til.",
            "code": "py",
            "terms": {
                "basic": [("print()", "Chop etish"), ("int", "Butun son"), ("str", "Satr"), ("bool", "Mantiqiy"), ("float", "Haqiqiy son")],
                "medium": [("list", "Ro'yxat"), ("dict", "Lug'at"), ("tuple", "Kortej"), ("set", "To'plam"), ("def", "Funksiya")],
                "high": [("class", "Sinf"), ("inheritance", "Merosxo'rlik"), ("polymorphism", "Polimorfizm"), ("lambda", "Nomsiz funksiya"), ("yield", "Generator")],
                "expert": [("GIL", "Global Interpreter Lock"), ("Metaclass", "Sinflarni yaratuvchi sinf"), ("Decorator", "Funksiya bezagi"), ("Context Manager", "with operatori"), ("Asyncio", "Asinxron dasturlash")]
            }
        },
        {
            "name": "Django Framework", 
            "desc": "Python da mukammal veb saytlar yaratish.",
            "code": "dj",
            "terms": {
                "basic": [("Model", "Ma'lumotlar tuzilmasi"), ("View", "Mantiqiy qism"), ("Template", "Ko'rinish"), ("URL", "Manzil"), ("Admin", "Boshqaruv paneli")],
                "medium": [("ORM", "Object-Relational Mapping"), ("QuerySet", "Ma'lumotlar so'rovi"), ("Context", "Shablon ma'lumotlari"), ("Form", "Ma'lumot kiritish"), ("Migration", "DB o'zgarishlari")],
                "high": [("Middleware", "Oraliq dastur"), ("Signal", "Hodisalar"), ("Mixin", "Qo'shimcha funksional"), ("CBV", "Class Based Views"), ("Serializer", "JSON o'giruvchi")],
                "expert": [("Channels", "WebSockets"), ("Celery", "Orqa fon vazifalari"), ("Cache", "Keshlash"), ("Optimizing", "Tezlashtirish"), ("Security", "Xavfsizlik")]
            }
        },
        {
            "name": "JavaScript", 
            "desc": "Veb sahifalarni interaktiv qilish.",
            "code": "js",
            "terms": {
                "basic": [("var/let/const", "O'zgaruvchilar"), ("function", "Funksiya"), ("alert", "Xabar oynasi"), ("console.log", "Konsolga yozish"), ("if/else", "Shart operatori")],
                "medium": [("DOM", "Document Object Model"), ("Event", "Hodisa"), ("Array", "Massiv"), ("Object", "Obyekt"), ("Loop", "Tsikl")],
                "high": [("Promise", "Va'da (Asinxron)"), ("Async/Await", "Kutish"), ("Closure", "Yopiq funksiya"), ("Callback", "Qayta chaqirish"), ("ES6", "Yangi standart")],
                "expert": [("Prototype", "Prototip"), ("V8 Engine", "JS Dvigateli"), ("Event Loop", "Hodisalar halqasi"), ("WebAssembly", "Yuqori tezlik"), ("Modules", "Modullar")]
            }
        },
        {
            "name": "HTML & CSS", 
            "desc": "Veb sahifa tuzilishi va dizayni.",
            "code": "html",
            "terms": {
                "basic": [("div", "Blog"), ("span", "Satr ichi"), ("h1-h6", "Sarlavhalar"), ("img", "Rasm"), ("a", "Havola")],
                "medium": [("Flexbox", "Egiluvchan quti"), ("Grid", "To'r"), ("Position", "Joylashuv"), ("Margin/Padding", "Bo'shliqlar"), ("Color", "Rang")],
                "high": [("Animation", "Animatsiya"), ("Transition", "O'tish"), ("Transform", "O'zgartirish"), ("Media Query", "Moslashuvchanlik"), ("Pseudo-class", "Soxta sinf")],
                "expert": [("Canvas", "Chizma"), ("SVG", "Vektor grafika"), ("SEO", "Qidiruv optimizatsiyasi"), ("Accessibility", "Qulaylik"), ("Shadow DOM", "Yopiq DOM")]
            }
        },
        {
            "name": "Algoritmlar", 
            "desc": "Mantiqiy fikrlash va muammolarni yechish.",
            "code": "algo",
            "terms": {
                "basic": [("Linear Search", "Chiziqli qidiruv"), ("Max/Min", "Eng katta/kichik"), ("Swap", "Almashtirish"), ("Counter", "Sanagich"), ("Sum", "Yig'indi")],
                "medium": [("Binary Search", "Ikki tomonlama qidiruv"), ("Bubble Sort", "Pufakchali saralash"), ("Stack", "Stek"), ("Queue", "Navbat"), ("Recursion", "Rekursiya")],
                "high": [("Quick Sort", "Tez saralash"), ("Merge Sort", "Birlashtirib saralash"), ("Hash Map", "Xesh jadval"), ("Tree", "Daraxt"), ("Graph", "Graf")],
                "expert": [("DP", "Dinamik dasturlash"), ("Dijkstra", "Eng qisqa yo'l"), ("Big O", "Murakkablik"), ("NP", "Murakkab muammolar"), ("Greedy", "Ochko'z algoritmlar")]
            }
        }
    ]

    difficulties = [
        ("Boshlang'ich", 1, 15, "basic"),
        ("O'rta", 2, 20, "medium"),
        ("Yuqori", 3, 25, "high"),
        ("Ekspert", 4, 30, "expert")
    ]

    total_questions_created = 0

    for subj_data in subjects_data:
        subject = Subject.objects.create(name=subj_data["name"], description=subj_data["desc"])
        print(f"Added Subject: {subject.name}")

        for diff_name, diff_order, diff_duration, term_key in difficulties:
            module = Module.objects.create(
                subject=subject,
                name=f"{diff_name} daraja",
                order=diff_order,
                description=f"{subject.name} bo'yicha {diff_name.lower()} bilimlar.",
                duration=diff_duration
            )
            
            # Generate 50 questions for this module
            terms = subj_data["terms"][term_key]
            
            for i in range(1, 51):
                # Cycle through terms to generate varied questions
                term_name, term_desc = terms[i % len(terms)]
                
                # Formula based math questions for variation if needed, but here we focus on Terminology
                # We will create 2 types of questions: Definition based and "What is X?"
                
                if i % 2 == 0:
                    q_text = f"{subject.name} ({diff_name}): '{term_name}' atamasi nimani anglatadi? (Savol {i})"
                    correct_text = term_desc
                    wrong_1 = f"{term_name} bu fayl nomi"
                    wrong_2 = f"{term_name} bu xato turi"
                    wrong_3 = f"{term_name} bu internet protokoli"
                else:
                    q_text = f"{subject.name} ({diff_name}): {term_desc} uchun qaysi atama ishlatiladi? (Savol {i})"
                    correct_text = term_name
                    # Pick wrong answers from other terms in the same set
                    wrong_1 = terms[(i + 1) % len(terms)][0]
                    wrong_2 = terms[(i + 2) % len(terms)][0]
                    wrong_3 = terms[(i + 3) % len(terms)][0]

                q = Question.objects.create(
                    module=module,
                    text=q_text,
                    marks=5
                )
                
                Choice.objects.create(question=q, text=correct_text, is_correct=True)
                Choice.objects.create(question=q, text=wrong_1, is_correct=False)
                Choice.objects.create(question=q, text=wrong_2, is_correct=False)
                Choice.objects.create(question=q, text=wrong_3, is_correct=False)
                
                total_questions_created += 1

    print(f"Jami {total_questions_created} ta savol va ma'lumotlar bazasi muvaffaqiyatli yaratildi!")

if __name__ == '__main__':
    seed()
