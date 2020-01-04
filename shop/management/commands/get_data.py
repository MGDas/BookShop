from time import time
from django.core.management.base import BaseCommand
from shop.parsers.get_genre import main as genres
from shop.parsers.get_book import main as book


class Command(BaseCommand):

    def handle(self, *args, **options):
        start = time()
        book()
        # genres()
        print(time() - start)
