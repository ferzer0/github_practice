from secrets import choice
import django_filters
from django_filters import DateFilter, CharFilter
from .models import *


class OrderFilter(django_filters.FilterSet):
    
    title = CharFilter(field_name="title", lookup_expr='icontains', label='Title')
  
    class Meta:
        model = Book
        fields = ['title', 'status']

    # def get_location(self, obj):
    #     return obj.Book.objects.exclude(location__isnull=True).exclude(location__exact='')

  