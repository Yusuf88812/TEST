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
            total_questions=20, # Always 20 questions
            start_time=timezone.now()
        )
        
        # Select 20 random questions for this attempt
        import random
        all_questions = list(module.questions.all())
        # If less than 20, take all, otherwise take 20 random
        selected_questions = random.sample(all_questions, min(len(all_questions), 20))
        
        # Create persistent answer placeholders for these questions
        for question in selected_questions:
            TestAnswer.objects.create(
                attempt=attempt,
                question=question
            )
    
    if attempt.completed:
        return redirect('quiz:test_result', attempt_id=attempt.id)

    # Get the questions associated with this specific attempt
    # We order by ID strictly to keep them consistent during the attempt
    # or random order if desired, but consistent per refresh 
    attempt_answers = attempt.answers.all().select_related('question').order_by('id')
    questions = [answer.question for answer in attempt_answers]
    
    # Prefetch choices for these specific questions to avoid N+1
    # Since we have question objects, we need to fetch choices efficiently.
    # The template iterates question.choices.all. 
    # We can rely on Django's caching or prefetch manually but for now let's leave it simple
    # as we already have the question objects. Ideally we would prefetch_related_objects(questions, 'choices')
    from django.db.models import prefetch_related_objects
    prefetch_related_objects(questions, 'choices')

    # Check timer
    elapsed_time = (timezone.now() - attempt.start_time).total_seconds()
    time_limit_seconds = module.duration * 60
    remaining_seconds = max(0, time_limit_seconds - elapsed_time)
    
    if request.method == 'POST':
        # PROCESS SUBMISSION
        score = 0
        correct_count = 0
        
        # We process the EXISTING TestAnswer objects for this attempt
        for answer in attempt_answers:
            question = answer.question
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
                pass
            
            # Update the existing answer object
            answer.selected_choice = selected_choice
            answer.code_answer = code_answer
            answer.is_correct = is_correct
            answer.save()
            
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
