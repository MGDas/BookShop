from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from shop.models import Genre


@admin.register(Genre)
class GenreMPTTModelAdmin(MPTTModelAdmin):
    mptt_level_indent = 20
