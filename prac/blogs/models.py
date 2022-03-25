from django.db import models
from django.utils import timezone
import datetime
from users.models import CustomUser

# Create your models here.
class Blog(models.Model):
    title = models.CharField(max_length=300)
    content = models.TextField()
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title 

    def __str__(self):
        return self.author
    
    def __str__(self):
        return self.content

class Blog_Likes(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    is_liked = models.BooleanField()
    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

class Blog_Comments(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.content
    
    def __str__(self):
        return self.author