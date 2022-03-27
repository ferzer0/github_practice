import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.views.generic import TemplateView
from email import contentmanager
from .models import Book, BookComments, BorrowedBook
from .forms import BookingForm, CommentForm
from user.forms import SettingForm
from django.contrib import messages
from django.contrib.auth.models import User
from .filters import OrderFilter
from django.core.exceptions import PermissionDenied
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.core.exceptions import PermissionDenied, ValidationError

# Create your views here.
class IndexView(TemplateView):
    template_name = "book/index.html"

    def get(self, request):
        books = Book.objects.order_by('-date_added')
        bookFilter = OrderFilter(request.GET, queryset=books)
        books = bookFilter.qs
        return render(request, self.template_name, {'books': books, 'filter': bookFilter})


class AddBookView(TemplateView):
    template_name = "book/addbook.html"

    def get(self, request):
        form = BookingForm()
        context = {'form':form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = BookingForm(request.POST)

        
        if form.is_valid():
            book = form.save(commit=False)
            book.user = request.user
            book.status = "Available"
            book.save()

        return redirect('book:index')


class DetailView(TemplateView):
    template_name = "book/detail.html"

    def get(self, request, **kwargs):
        comments = CommentForm()
        book = Book.objects.get(pk=self.kwargs.get('pk'))
        commented = BookComments.objects.filter(book=book)
        context = {'book':book, 'comments':comments, 'comment':commented}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        comments = CommentForm(request.POST)
        book = Book.objects.get(pk=self.kwargs.get('pk'))
        if comments.is_valid():
            new_comment = comments.save(commit=False)
            new_comment.author = request.user
            new_comment.book = book
            new_comment.save()
            return redirect('book:detail', book.pk)
           
class UpdateComment(TemplateView):
    template_name = "book/edit_comment.html"

    def get(self, request, **kwargs):
        comment = BookComments.objects.get(pk=self.kwargs.get('pk'))
     
        if comment.author == request.user:
            comment_form = CommentForm(instance=comment)
            context = {'comment_form': comment_form}
        else:
            raise PermissionDenied()
            
        return render(request, self.template_name, context)

    def post(self, request, **kwargs):

        comment = BookComments.objects.get(pk=self.kwargs.get('pk'))
        form = CommentForm(request.POST, instance=comment)
        
        if form.is_valid():
           form.save()
        return redirect('book:detail', comment.book.pk)

class DeleteComment(TemplateView):
    template_name = "book/detail.html"

    def post(self, request, **kwargs):
        comment = BookComments.objects.get(pk=self.kwargs.get('pk'))
        comment.delete()
        return redirect('book:detail', comment.book.pk)


class SettingView(TemplateView):
    template_name = "book/settings.html"

    def get(self, request):
        form = SettingForm(instance=request.user)
        context = {'form':form}
        return render(request, self.template_name, context)

    def post(self, request):
        form = SettingForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, f'Update Success')

        return redirect('book:settings')

class OwnedBookView(TemplateView):
    template_name = "book/ownedbook.html"

    def get(self, request):  
            books = Book.objects.filter(user=request.user)  
            return render(request, self.template_name, {'books':books})

class UpdateBookView(TemplateView):
    template_name = "book/update.html"

    def get(self, request, **kwargs):
        book = Book.objects.get(pk=self.kwargs.get('pk'))
        
        if book.user == request.user:
            form = BookingForm(instance=book)
            context = {'form': form}
        else:
            raise PermissionDenied()
            
        return render(request, self.template_name, context)
        
    def post(self, request, **kwargs):
        book = Book.objects.get(pk=self.kwargs.get('pk'))
        form = BookingForm(request.POST, instance=book)
        
        if form.is_valid():
            form.save()
        return redirect('book:owned')
        

class DeleteBookView(TemplateView):
    template_name = "book/deletebook.html"

    def get(self, request, **kwargs):
        book = Book.objects.get(pk=self.kwargs.get('pk'))
        if book.user == request.user: 
            context = {'book': book} 
        return render(request, self.template_name, context)
    
    def post(self, request, **kwargs):
        book = Book.objects.get(pk=self.kwargs.get('pk'))
        book.delete()
        return redirect('book:owned')

class BorrowedView(TemplateView):
    template_name = "book/borrowedbook.html"

    def get(self, request, **kwargs):
        borrow = BorrowedBook.objects.filter(borrower=request.user)
        return render(request, self.template_name, {'borrowed_book':borrow})

    def post(self, request, **kwargs): 
        book = Book.objects.get(pk=self.kwargs.get('pk'))
        checkout = BorrowedBook.objects.create(book=book, borrower=request.user)    

        if book.status == "Available":
            book.status = "Borrowed"
            book.save()
        
        return redirect('book:index')


class ReturnView(TemplateView):
    template_name = "book/borrowedbook.html"

    def post(self, request, **kwargs):
        book_borrow = BorrowedBook.objects.get(pk=self.kwargs.get('pk')) 
        date_now = datetime.datetime.now()
      
        if book_borrow.book.status == "Borrowed":
            book_borrow.book.status = "Available"
            book_borrow.return_date = date_now
            book_borrow.save()
            book_borrow.book.save()
        
        return redirect('book:borrowed_list')

def error403(request, exception):
    return render(request, 'book/403_csrf.html')