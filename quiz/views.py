from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.db.models import Sum
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Subject, Module, Question, Choice, TestAttempt, TestAnswer, Feedback

def home(request):
    subjects = Subject.objects.all()
    return render(request, 'quiz/home.html', {'subjects': subjects})

def subject_detail(request, subject_slug):
    subject = get_object_or_404(Subject, slug=subject_slug)
    modules = subject.modules.all()
    return render(request, 'quiz/subject_detail.html', {'subject': subject, 'modules': modules})



@login_required
def take_test(request, module_id):
    module = get_object_or_404(Module, pk=module_id)
    
    # Get or create attempt for this user/module
    # Check if there is an uncompleted attempt
    attempt = TestAttempt.objects.filter(
        module=module,
        user=request.user,
        completed=False
    ).first()

    if not attempt:
        # Create new attempt
        attempt = TestAttempt.objects.create(
            module=module,
            user=request.user,
            total_questions=module.questions.count(),
            start_time=timezone.now()
        )
    
    # If attempt is already completed (should use the filtered query above, but just in case of race/logic)
    if attempt.completed:
        return redirect('quiz:test_result', attempt_id=attempt.id)

    questions = module.questions.all().prefetch_related('choices')

    # Check timer
    elapsed_time = (timezone.now() - attempt.start_time).total_seconds()
    time_limit_seconds = module.duration * 60
    remaining_seconds = max(0, time_limit_seconds - elapsed_time)
    
    # Auto-submit if time is up (handled by frontend usually, but backend check is good)
    # logic: if post or time up...
    
    if request.method == 'POST':
        # PROCESS SUBMISSION
        score = 0
        correct_count = 0
        
        # Clear old answers for this attempt before saving new
        attempt.answers.all().delete()
        
        for question in questions:
            selected_choice_id = request.POST.get(f'question_{question.id}')
            is_correct = False
            selected_choice = None
            code_answer = None

            if question.question_type == 'MCQ':
                if selected_choice_id:
                    try:
                        selected_choice = Choice.objects.get(pk=selected_choice_id)
                        if selected_choice.is_correct:
                            score += question.marks
                            correct_count += 1
                            is_correct = True
                    except Choice.DoesNotExist:
                        pass
            elif question.question_type == 'CODE':
                code_answer = request.POST.get(f'code_answer_{question.id}')
                # Manual grading needed, or default correct? 
                # Let's mark as 0 score for now until graded.
                pass
            
            TestAnswer.objects.create(
                attempt=attempt,
                question=question,
                selected_choice=selected_choice,
                code_answer=code_answer,
                is_correct=is_correct
            )
            
        attempt.score = score
        attempt.correct_answers = correct_count
        attempt.completed = True
        attempt.completed_at = timezone.now()
        attempt.save()
        
        return redirect('quiz:test_result', attempt_id=attempt.id)
        
    return render(request, 'quiz/take_test.html', {
        'module': module,
        'questions': questions,
        'remaining_seconds': remaining_seconds,
        'attempt': attempt
    })

def test_result(request, attempt_id):
    attempt = get_object_or_404(TestAttempt, pk=attempt_id)
    return render(request, 'quiz/test_result.html', {'attempt': attempt})

def test_result_detail(request, attempt_id):
    attempt = get_object_or_404(TestAttempt, pk=attempt_id)
    answers = attempt.answers.all().select_related('question', 'selected_choice')
    return render(request, 'quiz/test_result_detail.html', {'attempt': attempt, 'answers': answers})

def leaderboard(request):
    # Top 50 scores across all modules
    top_attempts = TestAttempt.objects.select_related('module').order_by('-score', 'date_taken')[:50]
    return render(request, 'quiz/leaderboard.html', {'top_attempts': top_attempts})
@login_required
def profile(request):
    attempts = TestAttempt.objects.filter(user=request.user, completed=True).order_by('-date_taken')
    total_attempts = attempts.count()
    total_score = attempts.aggregate(Sum('score'))['score__sum'] or 0
    avg_score = 0
    if total_attempts > 0:
        avg_score = round(total_score / total_attempts, 1)
        
    return render(request, 'quiz/profile.html', {
        'attempts': attempts, 
        'total_attempts': total_attempts,
        'total_score': total_score,
        'avg_score': avg_score
    })

@login_required
def certificate(request, attempt_id):
    attempt = get_object_or_404(TestAttempt, pk=attempt_id, user=request.user, completed=True)
    
    total_marks = attempt.module.questions.aggregate(Sum('marks'))['marks__sum'] or 0
    percentage = 0
    if total_marks > 0:
        percentage = (attempt.score / total_marks) * 100
    
    return render(request, 'quiz/certificate.html', {
        'attempt': attempt, 
        'percentage': round(percentage, 1),
        'passed': percentage >= 70
    })
