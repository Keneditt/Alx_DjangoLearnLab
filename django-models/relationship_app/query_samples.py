import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

from relationship_app.models import Author, Book, Library, Librarian

# 1. Create sample data
print("--- Creating sample data ---")
try:
    # Create authors
    author1 = Author.objects.create(name="Stephen King")
    author2 = Author.objects.create(name="J.K. Rowling")

    # Create books
    book1 = Book.objects.create(title="It", author=author1)
    book2 = Book.objects.create(title="The Shining", author=author1)
    book3 = Book.objects.create(title="Harry Potter and the Sorcerer's Stone", author=author2)

    # Create libraries and associate books
    library1 = Library.objects.create(name="City Library")
    library1.books.set([book1, book3])  # Set books in the library

    library2 = Library.objects.create(name="Community Library")
    library2.books.set([book2, book3])

    # Create librarians
    librarian1 = Librarian.objects.create(name="Jane Doe", library=library1)
    librarian2 = Librarian.objects.create(name="John Smith", library=library2)
    print("Sample data created successfully!")

except Exception as e:
    print(f"Error creating data: {e}")
    print("The data might already exist or you need to run `makemigrations` and `migrate`.")
    print("Please run `python manage.py makemigrations` and `python manage.py migrate` first.")
    # Exit to prevent errors on subsequent queries
    exit()

print("\n--- Running queries ---")

# 2. Query all books by a specific author
print("Querying all books by 'Stephen King':")
books_by_author = Book.objects.filter(author__name="Stephen King")
for book in books_by_author:
    print(f"- {book.title}")

# 3. List all books in a library
print("\nListing all books in 'City Library':")
library_with_books = Library.objects.get(name="City Library")
books_in_library = library_with_books.books.all()
for book in books_in_library:
    print(f"- {book.title} by {book.author.name}")

# 4. Retrieve the librarian for a library
print("\nRetrieving the librarian for 'Community Library':")
try:
    library_to_query = Library.objects.get(name="Community Library")
    librarian = library_to_query.librarian
    print(f"The librarian for 'Community Library' is: {librarian.name}")
except Librarian.DoesNotExist:
    print("No librarian found for this library.")
