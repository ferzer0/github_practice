from django.urls import path
from django.views.generic import TemplateView
from blogs.views import IndexView, DetailView, AddView
from unittest import result
from . import views

app_name = 'blogs'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('detail/<int:pk>', DetailView.as_view(), name='detail'),
    path('add/', AddView.as_view(), name='add'),
]
