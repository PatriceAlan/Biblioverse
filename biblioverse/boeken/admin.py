from django.contrib import admin
from .models import Book, Review, Bookmark, Category, Author


# Register your models here.
admin.site.register(Book)
admin.site.register(Review)
admin.site.register(Bookmark)
admin.site.register(Category)
admin.site.register(Author)