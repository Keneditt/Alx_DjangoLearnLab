from django.urls import path
from . import views

urlpatterns = [
    # URL for adding a book
    path('books/create/', views.add_book, name='add-book'),
    
    # URL for editing a book by primary key
    path('books/update/<int:pk>/', views.edit_book, name='edit-book'),
    
    # URL for deleting a book by primary key
    path('books/delete/<int:pk>/', views.delete_book, name='delete-book'),
]
