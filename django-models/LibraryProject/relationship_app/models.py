from django.db import models

# Create your models here.
from django.db import models

class Author(models.Model):
    """
    Represents an author of a book.
    """
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Book(models.Model):
    """
    Represents a book in the library.
    It has a ForeignKey to Author, as a book is written by one author.
    """
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Library(models.Model):
    """
    Represents a library.
    A library can have many books, and a book can be in many libraries.
    """
    name = models.CharField(max_length=200)
    books = models.ManyToManyField(Book)

    def __str__(self):
        return self.name

class Librarian(models.Model):
    """
    Represents a librarian.
    It has a OneToOneField to Library, as each librarian is in charge of one library.
    """
    name = models.CharField(max_length=200)
    library = models.OneToOneField(Library, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
   