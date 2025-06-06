from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    photo = models.ImageField(upload_to='category_photos/', blank=True, null=True)

    def __str__(self):
        return self.name
    
class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    publication_date = models.DateField()
    genre = models.ForeignKey(Category, on_delete=models.CASCADE)
    summary = models.TextField()
    cover = models.ImageField(upload_to='book_covers/', blank=True, null=True)
    ebook_file = models.FileField(upload_to='ebooks/')
    added_by_admin = models.BooleanField(default=False)
    added_by_user = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title

class Review(models.Model):
    review_text = models.TextField()
    rating = models.PositiveIntegerField()
    review_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ebook = models.ForeignKey(Book, on_delete=models.CASCADE)

    def __str__(self):
        return f"Review by {self.user.username} for {self.ebook.title}"

class Bookmark(models.Model):
    page = models.PositiveBigIntegerField()
    bookmark_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ebook = models.ForeignKey(Book, on_delete=models.CASCADE)

    def __str__(self):
        return f"Bookmark by {self.user.username} for {self.ebook.title} at page {self.page}"
