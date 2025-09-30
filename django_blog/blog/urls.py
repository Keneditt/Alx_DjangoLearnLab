# blog/urls.py
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # CRUD URLs for Posts
    # Homepage/List View
    path('', views.PostListView.as_view(), name='post-list'),
    
    # Detail View (using post's primary key <pk>)
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
    
    # Create View (accessible only to logged-in users via LoginRequiredMixin)
    path('post/new/', views.PostCreateView.as_view(), name='post-create'),
    
    # Update View (accessible only to author via UserPassesTestMixin)
    path('post/<int:pk>/update/', views.PostUpdateView.as_view(), name='post-update'),
    
    # Delete View (accessible only to author via UserPassesTestMixin)
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post-delete'),

    # --- Existing Authentication URLs ---
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='blog/logout.html'), name='logout'),
]