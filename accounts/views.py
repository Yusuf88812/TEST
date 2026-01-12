from django.shortcuts import render, redirect
from django.contrib.auth import login
from quiz.forms import UserRegistrationForm

def signup(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('quiz:home')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/signup.html', {'form': form})
