from django.urls import path
from .views import list_books, LibraryDetailView

urlpatterns = [
    # Function-based view URL
    path('books/', list_books, name='book-list'),

    # Class-based view URL
    path('libraries/<int:pk>/', LibraryDetailView.as_view(), name='library-detail'),
]