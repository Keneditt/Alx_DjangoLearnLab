from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer

class BookListView(generics.ListAPIView):
    """
    ListView for retrieving all books with filtering and search capabilities.
    Allows read-only access to all users.
    """
    queryset = Book.objects.all().select_related('author')
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]  # Anyone can view books
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['author__name', 'publication_year']
    search_fields = ['title', 'author__name']
    ordering_fields = ['title', 'publication_year']
    ordering = ['title']  # Default ordering

class BookDetailView(generics.RetrieveAPIView):
    """
    DetailView for retrieving a single book by ID.
    Allows read-only access to all users.
    """
    queryset = Book.objects.all().select_related('author')
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]  # Anyone can view book details
    lookup_field = 'pk'

class BookCreateView(generics.CreateAPIView):
    """
    CreateView for adding a new book.
    Restricted to authenticated users only.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]  # Only authenticated users can create

    def perform_create(self, serializer):
        """
        Custom method to handle book creation.
        Can be extended to add custom logic like logging or notifications.
        """
        serializer.save()
        # Example: Log the creation (you'd need a logger set up)
        # logger.info(f"Book '{serializer.validated_data['title']}' created by {self.request.user}")

class BookUpdateView(generics.UpdateAPIView):
    """
    UpdateView for modifying an existing book.
    Restricted to authenticated users only.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]  # Only authenticated users can update
    lookup_field = 'pk'

    def perform_update(self, serializer):
        """
        Custom method to handle book updates.
        """
        serializer.save()
        # Example: Log the update
        # logger.info(f"Book '{self.get_object().title}' updated by {self.request.user}")

class BookDeleteView(generics.DestroyAPIView):
    """
    DeleteView for removing a book.
    Restricted to admin users only for safety.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAdminUser]  # Only admin users can delete
    lookup_field = 'pk'

    def perform_destroy(self, instance):
        """
        Custom method to handle book deletion with additional safety checks.
        """
        # Example: Add additional checks before deletion
        # if instance.has_related_records():
        #     raise ValidationError("Cannot delete book with related records")
        instance.delete()
        # logger.info(f"Book '{instance.title}' deleted by {self.request.user}")

# Author views for completeness
class AuthorListView(generics.ListCreateAPIView):
    """
    Combined List and Create view for Authors.
    Anyone can view, but only authenticated users can create authors.
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

class AuthorDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Combined Retrieve, Update, Delete view for Authors.
    Anyone can view, but only authenticated users can update/delete.
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'pk'