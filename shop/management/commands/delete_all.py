from django.core.management.base import BaseCommand
from shop.models import Book, Genre, Author


class Command(BaseCommand):

    def handle(self, *args, **options):
        # Genre.objects.all().delete()
        Author.objects.all().delete()
        Book.objects.all().delete()
        print('Deleted all!')
