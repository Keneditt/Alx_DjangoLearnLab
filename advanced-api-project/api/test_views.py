from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from api.models import Author, Book # Assuming your models are here

class BookAPITestCase(APITestCase):
    def setUp(self):
        # 1. Create a regular user for authentication tests
        self.user = User.objects.create_user(username='testuser', password='password')
        
        # 2. Create an admin user for delete tests
        self.admin_user = User.objects.create_superuser(username='admin', password='password')

        # 3. Create necessary related objects (Author)
        self.author_tolkien = Author.objects.create(name='J.R.R. Tolkien')
        self.author_rowling = Author.objects.create(name='J.K. Rowling')

        # 4. Create initial Book objects
        self.book1 = Book.objects.create(
            title='The Hobbit', author=self.author_tolkien, publication_year=1937
        )
        self.book2 = Book.objects.create(
            title='The Lord of the Rings', author=self.author_tolkien, publication_year=1954
        )
        self.book3 = Book.objects.create(
            title='Harry Potter', author=self.author_rowling, publication_year=1997
        )

        # 5. Define URLs for clarity
        self.list_url = reverse('book-list')
        self.detail_url = reverse('book-detail', kwargs={'pk': self.book1.pk})
        self.create_url = reverse('book-create') # Assuming you have this named URL

        self.valid_payload = {
            'title': 'New Book Title',
            'author': self.author_rowling.pk,
            'publication_year': 2020
        }

# =========================================================================
# 1. CRUD Operation Tests
# =========================================================================

    def test_list_books_success(self):
        """Ensure unauthenticated user can retrieve the book list."""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3) # Should return 3 books

    def test_retrieve_book_success(self):
        """Ensure unauthenticated user can retrieve a single book detail."""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'The Hobbit')

    def test_create_book_authenticated_success(self):
        """Ensure an authenticated user can create a new book."""
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.create_url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 4)
        self.assertEqual(response.data['title'], 'New Book Title')

    def test_update_book_authenticated_success(self):
        """Ensure an authenticated user can update a book."""
        self.client.force_authenticate(user=self.user)
        updated_data = {'title': 'Updated Title', 'publication_year': 1990, 'author': self.author_tolkien.pk}
        response = self.client.put(self.detail_url, updated_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Updated Title')

    def test_delete_book_admin_success(self):
        """Ensure only an admin user can delete a book."""
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(pk=self.book1.pk).exists())
        self.assertEqual(Book.objects.count(), 2)


# =========================================================================
# 2. Permission and Authentication Tests
# =========================================================================

    def test_create_book_unauthenticated_failure(self):
        """Ensure unauthenticated users cannot create books."""
        response = self.client.post(self.create_url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Book.objects.count(), 3)

    def test_update_book_unauthenticated_failure(self):
        """Ensure unauthenticated users cannot update books."""
        updated_data = {'title': 'Should Fail', 'publication_year': 2000, 'author': self.author_tolkien.pk}
        response = self.client.put(self.detail_url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.book1.refresh_from_db()
        self.assertNotEqual(self.book1.title, 'Should Fail')

    def test_delete_book_regular_user_failure(self):
        """Ensure regular authenticated users cannot delete books (Admin only)."""
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Book.objects.filter(pk=self.book1.pk).exists())


# =========================================================================
# 3. Filtering, Searching, and Ordering Tests
# =========================================================================

    def test_filter_by_author_success(self):
        """Ensure filtering by author (ID) works."""
        # Filter by Tolkien's ID
        response = self.client.get(f"{self.list_url}?author__name={self.author_tolkien.name}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2) # book1 and book2

    def test_search_by_title_success(self):
        """Ensure searching by book title works."""
        # Search for "Harry Potter"
        response = self.client.get(f"{self.list_url}?search=Harry+Potter")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Harry Potter')

    def test_ordering_by_year_descending(self):
        """Ensure ordering by publication_year descending works."""
        response = self.client.get(f"{self.list_url}?ordering=-publication_year")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # 1997 (HP), 1954 (LOTR), 1937 (Hobbit)
        self.assertEqual(response.data[0]['title'], 'Harry Potter')
        self.assertEqual(response.data[2]['title'], 'The Hobbit')