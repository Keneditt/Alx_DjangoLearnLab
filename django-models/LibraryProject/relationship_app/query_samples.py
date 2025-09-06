from relationship_app.models import Author, Book, Library

# Query all books by a specific author
def get_books_by_author(author_name):
    author = Author.objects.get(name=author_name)
    return Book.objects.filter(author=author)

# List all books in a Library
def get_books_in_library(library_name):
    library = Library.objects.get(name=library_name)
    return Library.objects.get(name=library_name).books.all()

# 4. Retrieve the librarian for a library
print("\nRetrieving the librarian for 'Community Library':")
try:
    library_to_query = Library.objects.get(name="Community Library")
    librarian = library_to_query.librarian
    print(f"The librarian for 'Community Library' is: {librarian.name}")
except librarian.DoesNotExist:
    print("No librarian found for this library.")
