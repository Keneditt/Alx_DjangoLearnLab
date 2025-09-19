from django.urls import path
from .views import list_books, LibraryDetailView

urlpatterns = [
    # Function-based view URL
    path('books/', list_books, name='book-list'),

    # Class-based view URL
    path('libraries/<int:pk>/', LibraryDetailView.as_view(), name='library-detail'),]

from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    # Other URL patterns for your app
    path('register/', views.register_view, name='register'),
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
]