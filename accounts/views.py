from django.contrib.auth import login
from django.contrib.auth.models import User
from django.shortcuts import redirect, render

from .forms import SignupForm
from .models import Owner


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
            )
            Owner.objects.create(
                user=user,
                city=form.cleaned_data['city'],
                phone=form.cleaned_data['phone'],
            )
            login(request, user)
            return redirect('accounts:home')
    else:
        form = SignupForm()
    return render(request, 'accounts/signup.html', {'form': form})


def home(request):
    return render(request, 'accounts/home.html')