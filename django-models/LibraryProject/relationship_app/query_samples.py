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
    author3 = Author.objects.create(name="Stephen King")
    
    # Create books
    book1 = Book.objects.create(title="Harry Potter and the Philosopher's Stone", author=author1)
    book2 = Book.objects.create(title="Harry Potter and the Chamber of Secrets", author=author1)
    book3 = Book.objects.create(title="A Game of Thrones", author=author2)
    book4 = Book.objects.create(title="The Shining", author=author3)
    
    # Create libraries and add books
    library1 = Library.objects.create(name="Central Library")
    library1.books.add(book1, book2, book3, book4)
    
    library2 = Library.objects.create(name="City Library")
    library2.books.add(book1, book3)
    
    # Create librarians
    librarian1 = Librarian.objects.create(name="Ms. Pince", library=library1)
    librarian2 = Librarian.objects.create(name="Mr. Filch", library=library2)
    
    return author1, author2, author3, library1, library2, librarian1, librarian2

def query_all_books_by_author(author_name):
    """Query all books by a specific author using Author.objects.get()"""
    try:
        author = Author.objects.get(name=author_name)
        books = Book.objects.filter(author=author)
        print(f"All books by {author_name} (using Author.objects.get()):")
        for book in books:
            print(f"- {book.title}")
        print()
        return books
    except Author.DoesNotExist:
        print(f"Author '{author_name}' does not exist.")
        return []

def query_all_books_by_author_alt(author_name):
    """Alternative way to query all books by a specific author"""
    books = Book.objects.filter(author__name=author_name)
    print(f"All books by {author_name} (using author__name filter):")
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
    author1, author2, author3, library1, library2, librarian1, librarian2 = create_sample_data()
    
    # Run the sample queries
    query_all_books_by_author("J.K. Rowling")
    query_all_books_by_author_alt("George R.R. Martin")
    list_all_books_in_library("Central Library")
    list_all_books_in_library("City Library")
    retrieve_librarian_for_library("Central Library")
    retrieve_librarian_for_library("City Library")
    
    # Additional demonstration of the specific queries mentioned
    print("=== Additional Demonstrations ===")
    
    # Using Author.objects.get(name=author_name)
    author = Author.objects.get(name="Stephen King")
    print(f"Author retrieved: {author.name}")
    
    # Using objects.filter(author=author)
    kings_books = Book.objects.filter(author=author)
    print("Stephen King's books:")
    for book in kings_books:
        print(f"- {book.title}")