from django.forms import ModelForm
from .models import Blog, Blog_Comments
from django import forms


class BlogForm(ModelForm):


    class Meta:
        model = Blog
        fields = ['title', 'content']


class CommentForm(forms.ModelForm):
    content = forms.CharField()
