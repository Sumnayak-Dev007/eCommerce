from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.views import LogoutView
from django.contrib.auth.decorators import login_required
# Create your views here.

def index(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login page after successful sign-up
    else:
        form = UserCreationForm()
    return render(request,'User/sign_up.html',{'form': form})

def CustomLogout(request):
    logout(request)  # Logs the user out
    return redirect('home')  # Redirect to home page