from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .forms import *

# Create your views here.

def index(request):
    return render(request, 'app/index.html')

def registro(request): 
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # Redirige a la página de inicio después del registro
    else:
        form = RegisterForm()
    return render(request,'registration/registro.html', {'form': form})