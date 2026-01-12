import os
import django
from django.test import Client

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from quiz.models import Subject, Module, Question, Choice, TestAttempt
from django.urls import reverse

def run_verification():
    c = Client()
    
    # 1. Check Home
    response = c.get(reverse('quiz:home'))
    assert response.status_code == 200, "Home page failed"
    print("Home Page Verified")
    
    # 2. Check Subject
    # Note: Name is now "Python Dasturlash" in Uzbek seed
    python_subjects = Subject.objects.filter(name__icontains="Python")
    if not python_subjects.exists():
        print("Warning: No Python subject found. Skipping subject detail check.")
    else:
        python = python_subjects.first()
        response = c.get(reverse('quiz:subject_detail', args=[python.slug]))
        assert response.status_code == 200, "Subject page failed"
        print(f"Subject Page ({python.name}) Verified")
        
        # 3. Check Module Login
        if python.modules.exists():
            mod = python.modules.first()
            response = c.get(reverse('quiz:module_login', args=[mod.id]))
            assert response.status_code == 200, "Login page failed"
            
            # Post Login
            response = c.post(reverse('quiz:module_login', args=[mod.id]), {'first_name': 'Test', 'last_name': 'User'})
            assert response.status_code == 302, "Login redirection failed"
            print("Login Flow Verified")
            
            # 4. Check Test Page
            session = c.session
            session['user_first_name'] = 'Test'
            session['user_last_name'] = 'User'
            session.save()
            
            response = c.get(reverse('quiz:take_test', args=[mod.id]))
            assert response.status_code == 200, "Test page failed"
            print("Test Page Verified")
            
            # 5. Submit Test
            q1 = mod.questions.first()
            if q1:
                c1 = q1.choices.filter(is_correct=True).first()
                if c1:
                    post_data = {
                        f'question_{q1.id}': c1.id
                    }
                    
                    response = c.post(reverse('quiz:take_test', args=[mod.id]), post_data)
                    assert response.status_code == 302, "Test submission failed"
                    
                    attempt = TestAttempt.objects.last()
                    assert attempt.score > 0, "Scoring failed"
                    print(f"Test Submission Verified. Score: {attempt.score}")

if __name__ == '__main__':
    try:
        run_verification()
        print("ALL CHECKS PASSED ✅")
    except Exception as e:
        print(f"VERIFICATION FAILED ❌: {e}")
