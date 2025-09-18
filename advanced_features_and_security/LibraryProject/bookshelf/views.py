from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from .models import Book
from .forms import BookForm

@login_required
def book_list(request):
    books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})

@permission_required('bookshelf.can_create', raise_exception=True)
def book_create(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save(commit=False)
            book.user = request.user
            book.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'bookshelf/book_form.html', {'form': form})

@permission_required('bookshelf.can_delete', raise_exception=True)
def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('book_list')
    return render(request, 'bookshelf/book_confirm_delete.html', {'book': book})

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from .models import Book
from .forms import BookForm, ExampleForm

@login_required
def book_list(request):
    books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})

@permission_required('bookshelf.can_create', raise_exception=True)
def book_create(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save(commit=False)
            book.user = request.user
            book.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'bookshelf/book_form.html', {'form': form})

@permission_required('bookshelf.can_delete', raise_exception=True)
def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('book_list')
    return render(request, 'bookshelf/book_confirm_delete.html', {'book': book})

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db import connection
from django.utils.html import escape
from .models import Book
from .forms import BookForm  # Assume you have a form defined

# Safe query using Django ORM
def book_list(request):
    # Safe - using Django ORM with parameterized queries
    books = Book.objects.filter(title__icontains=request.GET.get('q', ''))
    return render(request, 'bookshelf/book_list.html', {'books': books})

# UNSAFE EXAMPLE (for demonstration only - DO NOT USE)
def unsafe_book_search(request):
    query = request.GET.get('q', '')
    # UNSAFE - vulnerable to SQL injection
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT * FROM bookshelf_book WHERE title LIKE '%{query}%'")
        books = cursor.fetchall()
    return render(request, 'bookshelf/book_list.html', {'books': books})

# Safe form handling
@login_required
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            # Safe - using Django forms with validation
            form.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'bookshelf/add_book.html', {'form': form})

# Safe user input handling
def search_books(request):
    query = escape(request.GET.get('q', ''))  # Escape user input to prevent XSS
    books = Book.objects.filter(title__icontains=query)  # Safe ORM query
    return render(request, 'bookshelf/search_results.html', {
        'books': books,
        'query': query  # Note: query is escaped before rendering
    })