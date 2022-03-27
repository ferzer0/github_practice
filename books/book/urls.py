from django.urls import path
from django.views.generic import TemplateView
from . import views
from book.views import (
    IndexView, AddBookView, 
    SettingView, DetailView, 
    OwnedBookView, UpdateBookView, 
    DeleteBookView, BorrowedView,
    ReturnView, DeleteComment, UpdateComment,)
    
app_name = "book"

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('borrowedbook/', BorrowedView.as_view(), name='borrowed_list'),
    path('addBook/', AddBookView.as_view(), name='addbook'),
    path('settings/', SettingView.as_view(), name='settings'),
    path('detail/<int:pk>', DetailView.as_view(), name='detail'),
    path('ownedbook/', OwnedBookView.as_view(), name='owned'),
    path('updatebook/<int:pk>', UpdateBookView.as_view(), name='update'),
    path('deletebook/<int:pk>', DeleteBookView.as_view(), name='delete'),
    path('checkout/book/<int:pk>', BorrowedView.as_view(), name='borrowed'),
    path('return/book/<int:pk>', ReturnView.as_view(), name='return_book'),
    path('deletecomment/<int:pk>', DeleteComment.as_view(), name='delete_comment'),
    path('updatecomment/<int:pk>', UpdateComment.as_view(), name='update_comment'),
   
]
