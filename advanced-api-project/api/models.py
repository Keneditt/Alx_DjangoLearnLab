
from django.db import models

class Author(models.Model):
    """
    Author model representing a book author.
    
    Attributes:
        name (CharField): The name of the author (max length: 100 characters)
    """
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Book(models.Model):
    """
    Book model representing a published book.
    
    Attributes:
        title (CharField): The title of the book (max length: 200 characters)
        publication_year (IntegerField): The year the book was published
        author (ForeignKey): A reference to the Author of this book
    """
    title = models.CharField(max_length=200)
    publication_year = models.IntegerField()  # Added the missing publication_year field
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    
    def __str__(self):
        return self.title