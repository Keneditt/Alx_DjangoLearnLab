from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone

class Post(models.Model):
    """
    Blog Post model representing individual blog posts.
    """
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})
    
    def save(self, *args, **kwargs):
        """Set published_date to now if it's the first time being saved"""
        if not self.published_date:
            self.published_date = timezone.now()
        super().save(*args, **kwargs)
    
    class Meta:
        ordering = ['-published_date']