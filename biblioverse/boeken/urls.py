from . import views
from django.urls import path, include

urlpatterns = [
    path('', views.home, name='home'),
   path('categories/', views.book_categories, name='categories'),

    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
]
