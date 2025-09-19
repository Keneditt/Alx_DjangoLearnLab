from django.shortcuts import render
from .models import Library, Author
from django.views.generic import DetailView

def list_books(request):
    """
    A function-based view to list all books.
    """
    books = Library.objects.all()
    return render(request, 'list_books.html', {'books': books})

class LibraryDetailView(DetailView):
    """
    A class-based view to display details of a specific library.
    """
    model = Library
    template_name = 'library_detail.html'
    context_object_name = 'library'