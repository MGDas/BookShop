from time import time
from django.core.management.base import BaseCommand
from shop.parsers.genre import main as genre


class Command(BaseCommand):

    def handle(self, *args, **options):
        start = time()
        genre()
        print(time() - start)
