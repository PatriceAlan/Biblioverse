from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import SignUpForm
from django.db.models import Q
from .models import Category, Author, Book

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
        search_query = request.GET.get('search_query')

        if search_query:
            categories = categories.filter(Q(title__icontains=search_query))

        return render(request, 'categories.html', {'categories': categories, 'search_query': search_query})
    else:
        messages.error(request, "You must be logged in to view that page...")
        return redirect('home')

def book_authors(request):
    if request.user.is_authenticated:
        # Get a list of all authors with associated books
        authors_with_books = Author.objects.filter(book__isnull=False).distinct()

        # Create a dictionary to store authors grouped by the first letter
        author_dict = {}
        for author in authors_with_books:
            first_letter = author.first_name[0].upper()
            author_dict.setdefault(first_letter, []).append(author)

        # Sort the dictionary by keys
        sorted_author_dict = dict(sorted(author_dict.items()))

        context = {'author_dict': sorted_author_dict}
        return render(request, 'authors.html', context)
    
    else:
        messages.error(request, "You must be logged in to view that page...")
        return redirect('home')

def book_list(request):
    if request.user.is_authenticated:
        books = Book.objects.all()
        search_query = request.GET.get('search_query')

        if search_query:
            books = books.filter(Q(title__icontains=search_query))

        return render(request, 'books.html', {'books': books, 'search_query': search_query})
    else:
        messages.error(request, "You must be logged in to view that page...")
        return redirect('home')

def author_books(request, author_id):
    if request.user.is_authenticated:
        try:
            author = Author.objects.get(id=author_id)
        except Author.DoesNotExist:
            messages.error(request, "Author not found.")
            return redirect('home')

        author_books = Book.objects.filter(author=author)
        search_query = request.GET.get('search_query')

        if search_query:
            author_books = author_books.filter(Q(title__icontains=search_query))


        return render(request, 'author_books.html', {'author_books': author_books, 'author': author, 'search_query': search_query})
    else:
        messages.error(request, "You must be logged in to view that page...")
        return redirect('home')


def category_books(request, category_id):
    if request.user.is_authenticated:
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            messages.error(request, "Category not found.")
            return redirect('home')

        category_books = Book.objects.filter(genre=category)
        search_query = request.GET.get('search_query')

        if search_query:
            category_books = category_books.filter(Q(title__icontains=search_query))


        return render(request, 'category_books.html', {'category_books': category_books, 'category': category, 'search_query':search_query})
    else:
        messages.error(request, "You must be logged in to view that page...")
        return redirect('home')