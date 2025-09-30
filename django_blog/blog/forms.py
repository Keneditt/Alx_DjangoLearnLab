# blog/forms.py
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Post  # Import the Post model

# ... (Existing UserRegisterForm and UserUpdateForm remain unchanged) ...

class PostForm(forms.ModelForm):
    """Form for creating and updating Post objects."""
    class Meta:
        model = Post
        # Exclude 'author' and 'published_date' as they are set automatically
        fields = ['title', 'content']