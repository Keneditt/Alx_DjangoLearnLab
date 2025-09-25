from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from api.models import Author, Book # Ensure these models exist

class BookAPITestCase(APITestCase):
    def setUp(self):
        # 1. Create users
        self.user = User.objects.create_user(username='testuser', password='password')
        self.admin_user = User.objects.create_superuser(username='admin', password='adminpassword')

        # 2. Create related objects (Author)
        self.author_tolkien = Author.objects.create(name='J.R.R. Tolkien')
        self.author_rowling = Author.objects.create(name='J.K. Rowling')

        # 3. Create initial Book objects
        self.book1 = Book.objects.create(
            title='The Hobbit', author=self.author_tolkien, publication_year=1937
        )
        # ... (book2 and book3 initialization omitted for brevity)

        # 4. Define URLs (Ensure these URL names are defined in your api/urls.py)
        self.list_url = reverse('book-list')
        self.detail_url = reverse('book-detail', kwargs={'pk': self.book1.pk})
        self.create_url = reverse('book-create') 

        self.valid_payload = {
            'title': 'New Book Title',
            'author': self.author_rowling.pk,
            'publication_year': 2020
        }

## Authenticated CRUD Tests

    def test_create_book_authenticated_success(self):
        """Ensure an authenticated user can create a new book."""
        # --- Using self.client.force_authenticate ---
        self.client.force_authenticate(user=self.user)
        
        response = self.client.post(self.create_url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_book_authenticated_success(self):
        """Ensure an authenticated user can update a book."""
        # --- Using self.client.force_authenticate ---
        self.client.force_authenticate(user=self.user)
        
        updated_data = {'title': 'Updated Title', 'publication_year': 1990, 'author': self.author_tolkien.pk}
        response = self.client.put(self.detail_url, updated_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_book_admin_success(self):
        """Ensure only an admin user can delete a book."""
        # --- Using self.client.force_authenticate ---
        self.client.force_authenticate(user=self.admin_user)
        
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

## Permission Failure Tests

    def test_create_book_unauthenticated_failure(self):
        """Ensure unauthenticated users cannot create books."""
        # No authentication provided
        response = self.client.post(self.create_url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_delete_book_regular_user_failure(self):
        """Ensure regular authenticated users cannot delete books (Admin only)."""
        # --- Using self.client.force_authenticate ---
        self.client.force_authenticate(user=self.user)
        
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)