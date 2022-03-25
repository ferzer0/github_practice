from django.contrib import admin
from .models import Blog, CustomUser, Blog_Comments
# Register your models here.

admin.site.register(Blog)
admin.site.register(Blog_Comments)
admin.site.register(CustomUser)