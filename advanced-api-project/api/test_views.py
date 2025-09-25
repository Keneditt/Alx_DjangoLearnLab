from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from api.models import Author, Book

class BookAPITestCase(APITestCase):
    def setUp(self):
        # 1. Create users
        self.user_password = 'password'
        self.admin_password = 'adminpassword'
        
        self.user = User.objects.create_user(username='testuser', password=self.user_password)
        self.admin_user = User.objects.create_superuser(username='admin', password=self.admin_password)

        # 2. Create necessary related objects (Author)
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

        # 4. Define URLs for clarity
        self.list_url = reverse('book-list')
        self.detail_url = reverse('book-detail', kwargs={'pk': self.book1.pk})
        self.create_url = reverse('book-create') 
        self.update_url = reverse('book-update', kwargs={'pk': self.book1.pk})
        self.delete_url = reverse('book-delete', kwargs={'pk': self.book1.pk})

        self.valid_payload = {
            'title': 'New Book Title',
            'author': self.author_rowling.pk,
            'publication_year': 2020
        }

    def tearDown(self):
        # Logout after each test to ensure clean state
        self.client.logout()

# =========================================================================
# 1. CRUD Operation Tests
# =========================================================================

    def test_list_books_success(self):
        """Ensure we can retrieve the list of books without authentication."""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 3)

    def test_retrieve_book_success(self):
        """Ensure we can retrieve a single book without authentication."""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'The Hobbit')

    def test_create_book_authenticated_success(self):
        """Ensure an authenticated user can create a new book using self.client.login."""
        # Use self.client.login
        self.client.login(username=self.user.username, password=self.user_password)
        
        response = self.client.post(self.create_url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 4)

    def test_update_book_authenticated_success(self):
        """Ensure an authenticated user can update a book using self.client.login."""
        # Use self.client.login
        self.client.login(username=self.user.username, password=self.user_password)
        
        updated_data = {'title': 'Updated Title', 'publication_year': 1990, 'author': self.author_tolkien.pk}
        response = self.client.put(self.update_url, updated_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Updated Title')

    def test_delete_book_admin_success(self):
        """Ensure only an admin user can delete a book using self.client.login."""
        # Use self.client.login
        self.client.login(username=self.admin_user.username, password=self.admin_password)
        
        response = self.client.delete(self.delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(pk=self.book1.pk).exists())


# =========================================================================
# 2. Permission and Authentication Tests
# =========================================================================

    def test_create_book_unauthenticated_failure(self):
        """Ensure unauthenticated users cannot create books."""
        response = self.client.post(self.create_url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_book_unauthenticated_failure(self):
        """Ensure unauthenticated users cannot update books."""
        updated_data = {'title': 'Updated Title'}
        response = self.client.put(self.update_url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_book_regular_user_failure(self):
        """Ensure regular authenticated users cannot delete books (Admin only) using self.client.login."""
        # Use self.client.login
        self.client.login(username=self.user.username, password=self.user_password)
        
        response = self.client.delete(self.delete_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Book.objects.filter(pk=self.book1.pk).exists())

    def test_delete_book_unauthenticated_failure(self):
        """Ensure unauthenticated users cannot delete books."""
        response = self.client.delete(self.delete_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


# =========================================================================
# 3. Filtering, Searching, and Ordering Tests (Authentication not strictly needed here)
# =========================================================================

    def test_filter_books_by_author(self):
        """Test filtering books by author name."""
        # No login needed for read operations
        response = self.client.get(self.list_url, {'author_name': 'Tolkien'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        
        for book in response.data['results']:
            self.assertIn('Tolkien', book['author_name'])

    def test_filter_books_by_publication_year(self):
        """Test filtering books by publication year."""
        # No login needed for read operations
        response = self.client.get(self.list_url, {'publication_year': 1997})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['publication_year'], 1997)

    def test_search_books_by_title(self):
        """Test searching books by title."""
        # No login needed for read operations
        response = self.client.get(self.list_url, {'search': 'Harry'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertIn('Harry', response.data['results'][0]['title'])

    def test_order_books_by_title_ascending(self):
        """Test ordering books by title ascending."""
        # No login needed for read operations
        response = self.client.get(self.list_url, {'ordering': 'title'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        titles = [book['title'] for book in response.data['results']]
        self.assertEqual(titles, sorted(titles))

    def test_order_books_by_publication_year_descending(self):
        """Test ordering books by publication year descending."""
        # No login needed for read operations
        response = self.client.get(self.list_url, {'ordering': '-publication_year'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        years = [book['publication_year'] for book in response.data['results']]
        self.assertEqual(years, sorted(years, reverse=True))

    def test_combined_filter_search_order(self):
        """Test combining filtering, searching, and ordering."""
        # No login needed for read operations
        response = self.client.get(self.list_url, {
            'author_name': 'Tolkien',
            'ordering': '-publication_year'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        
        # Should be ordered by publication year descending
        self.assertEqual(response.data['results'][0]['publication_year'], 1954)
        self.assertEqual(response.data['results'][1]['publication_year'], 1937)


# =========================================================================
# 4. Additional Tests with self.client.login
# =========================================================================

    def test_create_book_with_invalid_data(self):
        """Test creating a book with invalid data using self.client.login."""
        self.client.login(username=self.user.username, password=self.user_password)
        
        invalid_payload = {
            'title': '',  # Empty title
            'author': self.author_rowling.pk,
            'publication_year': 3000  # Future year
        }
        
        response = self.client.post(self.create_url, invalid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('title', response.data)
        self.assertIn('publication_year', response.data)

    def test_partial_update_book(self):
        """Test partial update of a book using PATCH and self.client.login."""
        self.client.login(username=self.user.username, password=self.user_password)
        
        partial_data = {'title': 'Partially Updated Title'}
        response = self.client.patch(self.update_url, partial_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Partially Updated Title')
        # Other fields should remain unchanged
        self.assertEqual(self.book1.publication_year, 1937)

    def test_create_book_admin_user(self):
        """Test that admin users can also create books using self.client.login."""
        self.client.login(username=self.admin_user.username, password=self.admin_password)
        
        response = self.client.post(self.create_url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 4)

    def test_update_book_admin_user(self):
        """Test that admin users can update books using self.client.login."""
        self.client.login(username=self.admin_user.username, password=self.admin_password)
        
        updated_data = {'title': 'Admin Updated Title', 'publication_year': 2000, 'author': self.author_tolkien.pk}
        response = self.client.put(self.update_url, updated_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Admin Updated Title')