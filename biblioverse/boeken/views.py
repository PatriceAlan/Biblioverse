from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import SignUpForm
from .models import Category

def home(request):
    if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, f"Login Successful. Welcome back {username} !")
                return redirect('home')
            else:
                messages.error(request, "Login Failed. Please check your credentials and try again...")
                return redirect('home')
    else:
        return render(request, 'home.html')

def logout_user(request):
    logout(request)
    messages.success(request, "Logout Successful. Don't hesitate to come again!")
    return redirect('home')

def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration Successful ! You can now log in using your credentials.")
            return redirect('home')
    else:
        form = SignUpForm()
    
    return render(request, 'register.html', {'form': form})

def book_categories(request):
    if request.user.is_authenticated:
        categories = Category.objects.all()
        return render(request, 'categories.html', {'categories': categories})
    else:
        messages.error(request, "You must be logged in to view that page...")
        return redirect('home')

def book_authors(request):
    if request.user.is_authenticated:

        author_users = User.objects.filter(book__isnull=False)

        author_users = author_users.distinct()

        context = { 'author_users': author_users}

        return render(request, 'authors.html', context)
    
    else:
        messages.error(request, "You must be logged in to view that page...")
        return redirect('home')