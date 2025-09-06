from relationship_app.models import Author, Book, Library

# Query all books by a specific author
def get_books_by_author(author_name):
    author = Author.objects.get(name=author_name)
    return Book.objects.filter(author=author)

# List all books in a Library
def get_books_in_library(library_name):
    library = Library.objects.get(name=library_name)
    return Library.objects.get(name=library_name).books.all()

# Find the library a specific book is in
def get_librarian_for_book(library_name):
    library = Library.objects.get(name=library_name)
    return library.objects.get(name=library_name).librarian
