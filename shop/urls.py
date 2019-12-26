from django.urls import path
from shop.views.base_view import BaseView


urlpatterns = [
    path('', BaseView.as_view(), name='base_url')
]