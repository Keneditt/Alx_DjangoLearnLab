from django.shortcuts import render
from django.views.generic import DetailView
from .models import Book, Library

# Function-based view to list all books
def list_books(request):
    """
    Renders a list of all books in the database.
    """
    books = Book.objects.all()
    context = {
        'books': books
    }
    return render(request, 'list_books.html', context)

# Class-based view to display details for a specific library
class LibraryDetailView(DetailView):
    """
    Displays details for a specific library, including all books it contains.
    """
    model = Library
    template_name = 'library_detail.html'
    context_object_name = 'library'
