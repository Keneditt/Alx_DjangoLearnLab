from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Book
from .serializers import BookSerializer

class BookListCreateView(generics.ListCreateAPIView):
    """
    API view to list all books or create a new book.
    - list(): GET request to retrieve all books.
    - create(): POST request to add a new book.
    Permissions: Read-only for unauthenticated users, allows creation for authenticated users.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    def get_permissions(self):
        """
        Customizes permissions based on the request method.
        """
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

class BookRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update, or delete a single book.
    - retrieve(): GET request for a single book.
    - update(): PUT/PATCH request to modify a book.
    - destroy(): DELETE request to remove a book.
    Permissions: Read-only for unauthenticated users, allows update/delete for authenticated users.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_permissions(self):
        """
        Customizes permissions based on the request method.
        """
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]
# Create your views here.
