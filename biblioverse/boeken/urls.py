from . import views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('categories/', views.book_categories, name='categories'),
    path('books/', views.book_list, name='books'),
    path('authors/', views.book_authors, name='authors'),
    path('author/<int:author_id>/books/', views.author_books, name='author_books'),
    path('category/<int:category_id>/books/', views.category_books, name='category_books'),

    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)