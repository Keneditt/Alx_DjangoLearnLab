import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

from relationship_app.models import Author, Book, Library, Librarian

def create_sample_data():
    """Create sample data for testing queries"""
    # Create authors
    author1 = Author.objects.create(name="J.K. Rowling")
    author2 = Author.objects.create(name="George R.R. Martin")
    
    # Create books
    book1 = Book.objects.create(title="Harry Potter and the Philosopher's Stone", author=author1)
    book2 = Book.objects.create(title="Harry Potter and the Chamber of Secrets", author=author1)
    book3 = Book.objects.create(title="A Game of Thrones", author=author2)
    
    # Create a library and add books
    library = Library.objects.create(name="Central Library")
    library.books.add(book1, book2, book3)
    
    # Create a librarian
    librarian = Librarian.objects.create(name="Ms. Pince", library=library)
    
    return author1, library, librarian

def query_all_books_by_author(author_name):
    """Query all books by a specific author"""
    books = Book.objects.filter(author__name=author_name)
    print(f"All books by {author_name}:")
    for book in books:
        print(f"- {book.title}")
    print()
    return books

def list_all_books_in_library(library_name):
    """List all books in a library"""
    try:
        library = Library.objects.get(name=library_name)
        books = library.books.all()
        print(f"All books in {library_name}:")
        for book in books:
            print(f"- {book.title} by {book.author.name}")
        print()
        return books
    except Library.DoesNotExist:
        print(f"Library '{library_name}' does not exist.")
        return []

def retrieve_librarian_for_library(library_name):
    """Retrieve the librarian for a library"""
    try:
        library = Library.objects.get(name=library_name)
        librarian = Librarian.objects.get(library=library)
        print(f"Librarian for {library_name}: {librarian.name}")
        return librarian
    except (Library.DoesNotExist, Librarian.DoesNotExist):
        print(f"No librarian found for {library_name} or library doesn't exist.")
        return None

if __name__ == "__main__":
    # Create sample data
    author1, library, librarian = create_sample_data()
    
    # Run the sample queries
    query_all_books_by_author("J.K. Rowling")
    list_all_books_in_library("Central Library")
    retrieve_librarian_for_library("Central Library")