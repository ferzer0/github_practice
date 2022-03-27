from tkinter import CASCADE
from django.db import models
from django.utils import timezone
import datetime
from user.models import CustomUser

# Create your models here.

class Book(models.Model):
    CHOICE_STATUS = (
        ('Available', 'Available'),
        ('Borrowed', 'Borrowed'),
    )
    title = models.CharField(max_length=200, blank=False) 
    author = models.CharField(max_length=200, blank=False)
    location = models.CharField(max_length=100)
    status = models.CharField(max_length=200, choices=CHOICE_STATUS) 
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True) 
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} {} {}'.format(self.title, self.author, self.location)

    class Meta:
        ordering = ("-date_added",)

class BorrowedBook(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrower = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date_borrow = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return '{} {} '.format(self.book, self.borrower)

    class Meta:
        ordering = ("-date_borrow",)

class BookComments(models.Model):
    book = models.ForeignKey(Book, related_name="comments", on_delete=models.CASCADE)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)


    class Meta:
        ordering = ("-date_added",)

    def __str__(self):
        return '{}'.format(f"comment by {self.author}")
    
  
