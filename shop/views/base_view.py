from django.views.generic import ListView
from shop.models import Genre
from django.shortcuts import render


class BaseView(ListView):
    model = Genre
    template_name = 'base.html'
    context_object_name = 'genres'
