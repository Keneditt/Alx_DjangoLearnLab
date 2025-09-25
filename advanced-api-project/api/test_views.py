from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from api.models import Author, Book
import json

class BaseAPITestCase(APITestCase):
    """
    Base test case with common setup for all API tests.
    """
    
    def setUp(self):
        """
        Set up test data that will be used across multiple test cases.
        """
        # Create test users
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpass123'
        )
        self.regular_user = User.objects.create_user(
            username='testuser',
            email='user@example.com',
            password='testpass123'
        )
        self.another_user = User.objects.create_user(
            username='anotheruser',
            email='another@example.com',
            password='anotherpass123'
        )
        
        # Create test authors
        self.author1 = Author.objects.create(name="J.K. Rowling")
        self.author2 = Author.objects.create(name="George R.R. Martin")
        self.author3 = Author.objects.create(name="Stephen King")
        
        # Create test books
        self.book1 = Book.objects.create(
            title="Harry Potter and the Philosopher's Stone",
            publication_year=1997,
            author=self.author1
        )
        self.book2 = Book.objects.create(
            title="Harry Potter and the Chamber of Secrets",
            publication_year=1998,
            author=self.author1
        )
        self.book3 = Book.objects.create(
            title="A Game of Thrones",
            publication_year=1996,
            author=self.author2
        )
        self.book4 = Book.objects.create(
            title="The Shining",
            publication_year=1977,
            author=self.author3
        )
        
        # Create API client instances
        self.client = APIClient()
        self.admin_client = APIClient()
        self.user_client = APIClient()
        
        # Authenticate clients
        self.admin_client.force_authenticate(user=self.admin_user)
        self.user_client.force_authenticate(user=self.regular_user)