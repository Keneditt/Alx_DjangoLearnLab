from django.urls import path
from django.urls import path
from .views import BookListCreateView, BookRetrieveUpdateDestroyView

urlpatterns = [
    # URL for listing all books and creating a new book
    path('books/', BookListCreateView.as_view(), name='book-list-create'),

    # URL for retrieving, updating, or deleting a single book by its primary key (pk)
    path('books/<int:pk>/', BookRetrieveUpdateDestroyView.as_view(), name='book-detail'),
]