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
        self.book2 = Book.objects.create(
            title='The Lord of the Rings', author=self.author_tolkien, publication_year=1954
        )
        self.book3 = Book.objects.create(
            title='Harry Potter', author=self.author_rowling, publication_year=1997
        )

        # 4. Define URLs for clarity (Ensure these URL names are defined in your api/urls.py)
        self.list_url = reverse('book-list')
        self.detail_url = reverse('book-detail', kwargs={'pk': self.book1.pk})
        self.create_url = reverse('book-create') 

        self.valid_payload = {
            'title': 'New Book Title',
            'author': self.author_rowling.pk,
            'publication_year': 2020
        }

# =========================================================================
# 1. CRUD Operation Tests (Authenticated)
# =========================================================================

    def test_create_book_authenticated_success(self):
        """Ensure an authenticated user can create a new book."""
        # Authenticate the user for this request
        self.client.force_authenticate(user=self.user)
        
        response = self.client.post(self.create_url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 4)

    def test_update_book_authenticated_success(self):
        """Ensure an authenticated user can update a book."""
        # Authenticate the user for this request
        self.client.force_authenticate(user=self.user)
        
        updated_data = {'title': 'Updated Title', 'publication_year': 1990, 'author': self.author_tolkien.pk}
        response = self.client.put(self.detail_url, updated_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Updated Title')

    def test_delete_book_admin_success(self):
        """Ensure only an admin user can delete a book."""
        # Authenticate the admin user for this request
        self.client.force_authenticate(user=self.admin_user)
        
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(pk=self.book1.pk).exists())

# =========================================================================
# 2. Permission and Authentication Tests (Unauthenticated/Forbidden)
# =========================================================================
    
    def test_create_book_unauthenticated_failure(self):
        """Ensure unauthenticated users cannot create books."""
        # No authentication provided
        response = self.client.post(self.create_url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_delete_book_regular_user_failure(self):
        """Ensure regular authenticated users cannot delete books (Admin only)."""
        # Authenticate the regular user
        self.client.force_authenticate(user=self.user)
        
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Book.objects.filter(pk=self.book1.pk).exists())