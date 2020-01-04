from django.views.generic import ListView
from shop.models import Genre, Book
from django.shortcuts import render


class BaseView(ListView):
    template_name = 'base.html'
    queryset = Book.objects.all()
    context_object_name = 'books'
    paginate_by = 15
