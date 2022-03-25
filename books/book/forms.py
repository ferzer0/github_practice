from ast import Add
from django.forms import ModelForm
from .models import BorrowedBook, Book, BookComments
from django import forms
from django.core.exceptions import ValidationError


class BookingForm(ModelForm):
    title = forms.CharField(max_length=30,  required=False, help_text='', widget=forms.TextInput(attrs={'class':'form-control'}))
    author = forms.CharField(max_length=30, required=False, help_text='', widget=forms.TextInput(attrs={'class':'form-control'}))
    location = forms.CharField(max_length=30, required=False, help_text='', widget=forms.TextInput(attrs={'class':'form-control', 'id':'get_location'}))

    class Meta:
        model = Book
        fields = ['title', 'author', 'location']

    def clean(self):
        title = self.cleaned_data.get("title")
        author = self.cleaned_data.get("author")
        
        if title and author is None:
            raise forms.ValidationError("Title is required.")
        if author is not None and not title:
            raise forms.ValidationError("Author is required.")
        return self.cleaned_data

    def clean_title(self):
        if self.cleaned_data["title"].strip() == '':
            raise ValidationError("Title is required.")
        return self.cleaned_data["title"]

    def clean_author(self):
        if self.cleaned_data["author"].strip() == '':
            raise ValidationError("Author is required.")
        return self.cleaned_data["author"]

    def clean_location(self):
        if self.cleaned_data["location"].strip() == '':
            raise ValidationError("location is required.")
        return self.cleaned_data["location"]
    

class CommentForm(forms.ModelForm):
    content = forms.CharField(label="", widget=forms.Textarea(attrs={
        'rows': '4',
        'class': 'md-textarea form-control',
        'placeholder': 'comment here...'
    }))

    class Meta:
        model = BookComments
        fields = ['content']



