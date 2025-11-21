from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # صفحه اصلی
    path('books/', views.book_list, name='book_list'),
    path('books/<int:pk>/', views.book_detail, name='book_detail'),
    path('books/create/', views.book_create, name='book_create'),
    path('books/<int:pk>/edit/', views.book_update, name='book_update'),
    path('books/<int:pk>/delete/', views.book_delete, name='book_delete'),
    path('books/<int:pk>/toggle-read/', views.toggle_read, name='toggle_read'),
    path('books/form/', views.book_form, name='book_form'),

]