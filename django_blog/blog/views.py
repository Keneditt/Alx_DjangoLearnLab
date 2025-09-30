# blog/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.urls import reverse_lazy
from .forms import UserRegisterForm, UserUpdateForm, PostForm
from .models import Post

# --- Existing Authentication Views (register, profile) ---
# ... (Keep existing register and profile views) ...

# -------------------- CRUD VIEWS -----------------------

# Replaces the simple post_list function
class PostListView(ListView):
    """Displays a list of all blog posts."""
    model = Post
    template_name = 'blog/post_list.html'  # <app>/<model>_list.html
    context_object_name = 'posts'
    ordering = ['-published_date']
    paginate_by = 10

class PostDetailView(DetailView):
    """Displays a single blog post."""
    model = Post
    template_name = 'blog/post_detail.html'

class PostCreateView(LoginRequiredMixin, CreateView):
    """Allows authenticated users to create a new post."""
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    # Redirect to the detail view of the new post upon success
    success_url = reverse_lazy('post-list')

    def form_valid(self, form):
        # Automatically set the author to the currently logged-in user
        form.instance.author = self.request.user
        messages.success(self.request, "Your post has been created!")
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Allows the post author to update their post."""
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    
    def form_valid(self, form):
        # Ensure the author field remains the same (security)
        form.instance.author = self.request.user
        messages.info(self.request, "Your post has been updated!")
        return super().form_valid(form)

    def test_func(self):
        # Custom test: only the post author can update it
        post = self.get_object()
        return self.request.user == post.author

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Allows the post author to delete their post."""
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('post-list') # Redirect to the post list after deletion

    def delete(self, request, *args, **kwargs):
        messages.error(request, "Your post has been successfully deleted.")
        return super().delete(request, *args, **kwargs)

    def test_func(self):
        # Custom test: only the post author can delete it
        post = self.get_object()
        return self.request.user == post.author

# --- Existing simple function view (Replaced, but kept here for context) ---
# def post_list(request):
#     # This function is now superseded by PostListView
#     return render(request, 'blog/index.html', {})

# blog/views.py

class PostListView(ListView):
    # ...
    template_name = 'blog/post_list.html'  # Matches file post_list.html

class PostDetailView(DetailView):
    # ...
    template_name = 'blog/post_detail.html' # Matches file post_detail.html

class PostCreateView(LoginRequiredMixin, CreateView):
    # ...
    template_name = 'blog/post_form.html' # Matches file post_form.html

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    # ...
    template_name = 'blog/post_form.html' # Matches file post_form.html
    
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    # ...
    template_name = 'blog/post_confirm_delete.html' # Matches file post_confirm_delete.html