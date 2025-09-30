from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.contrib.auth.models import User
from django.db.models import Q
from .models import Post, UserProfile
from .forms import PostForm, CustomUserCreationForm, UserUpdateForm, ProfileUpdateForm

class PostListView(ListView):
    """
    Display a list of all blog posts with pagination and search functionality.
    Accessible to all users (authenticated and anonymous).
    """
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 5
    ordering = ['-published_date']
    
    def get_queryset(self):
        """Add search functionality to the post list"""
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search', '')
        
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(content__icontains=search_query) |
                Q(author__username__icontains=search_query)
            )
        
        return queryset
    
    def get_context_data(self, **kwargs):
        """Add additional context data"""
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        context['total_posts'] = Post.objects.count()
        return context

class UserPostListView(ListView):
    """
    Display posts by a specific user.
    """
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5
    
    def get_queryset(self):
        """Get posts for the specific user"""
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-published_date')
    
    def get_context_data(self, **kwargs):
        """Add user to context"""
        context = super().get_context_data(**kwargs)
        context['profile_user'] = get_object_or_404(User, username=self.kwargs.get('username'))
        return context

class PostDetailView(DetailView):
    """
    Display a single blog post in full detail.
    Accessible to all users.
    """
    model = Post
    template_name = 'blog/post_detail.html'
    
    def get_context_data(self, **kwargs):
        """Add additional context for the post detail view"""
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        
        # Get previous and next posts for navigation
        context['previous_post'] = Post.objects.filter(
            published_date__lt=post.published_date
        ).order_by('-published_date').first()
        
        context['next_post'] = Post.objects.filter(
            published_date__gt=post.published_date
        ).order_by('published_date').first()
        
        return context

class PostCreateView(LoginRequiredMixin, CreateView):
    """
    Allow authenticated users to create new blog posts.
    The author is automatically set to the current user.
    """
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    
    def form_valid(self, form):
        """Set the author to the current user before saving"""
        form.instance.author = self.request.user
        messages.success(
            self.request, 
            'Your post has been created successfully!'
        )
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        """Add context for the create view"""
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create New Post'
        context['submit_text'] = 'Create Post'
        return context

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Allow post authors to update their existing posts.
    Only the author can edit their own posts.
    """
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    
    def form_valid(self, form):
        """Set success message on update"""
        messages.success(
            self.request, 
            'Your post has been updated successfully!'
        )
        return super().form_valid(form)
    
    def test_func(self):
        """Ensure only the author can update the post"""
        post = self.get_object()
        return self.request.user == post.author
    
    def get_context_data(self, **kwargs):
        """Add context for the update view"""
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update Post'
        context['submit_text'] = 'Update Post'
        return context

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Allow post authors to delete their posts.
    Only the author can delete their own posts.
    """
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = '/'
    
    def test_func(self):
        """Ensure only the author can delete the post"""
        post = self.get_object()
        return self.request.user == post.author
    
    def delete(self, request, *args, **kwargs):
        """Set success message on delete"""
        messages.success(
            request, 
            'Your post has been deleted successfully!'
        )
        return super().delete(request, *args, **kwargs)

# ... (keep existing profile and registration views) ...