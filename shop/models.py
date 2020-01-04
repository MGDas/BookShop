from mptt.models import MPTTModel, TreeForeignKey
from django.db import models
from slugify import slugify


def save_image_book(instance, filename):
    file = '.'.join([slugify(instance.name[:21]), filename.split('.')[-1]])
    return '/'.join([f'authors/{instance.author.slug}/books', file])


class BaseModel(models.Model):

    def __str__(self):
        if self.name:
            return self.name

    class Meta:
        abstract = True


class Author(BaseModel):
    name = models.CharField(max_length=500, db_index=True)
    slug = models.SlugField(max_length=500, unique=True)

    class Meta:
        db_table = 'author'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name) + f'-{self.pk}'
        return super().save(*args, **kwargs)


class Genre(MPTTModel, BaseModel):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, blank=True, null=True)
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )

    class Meta:
        db_table = 'genre'


class Book(BaseModel):
    author = models.ForeignKey(
        Author,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='books'
    )

    genre = models.ForeignKey(
        Genre,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='books'
    )

    name = models.CharField(max_length=500, db_index=True)
    photo_url = models.URLField(max_length=500, blank=True, null=True)

    class Meta:
        db_table = 'book'
