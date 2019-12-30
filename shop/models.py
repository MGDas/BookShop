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
    name = models.CharField(max_length=250, db_index=True)
    slug = models.SlugField(max_length=250, unique=True)

    class Meta:
        db_table = 'author'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name) + f'-{self.pk}'
        return super().save(*args, **kwargs)


class Genre(MPTTModel, BaseModel):
    name = models.CharField(max_length=100, db_index=True)
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
    description = models.TextField(blank=True)
    public_year = models.CharField(max_length=4, blank=True)
    count_page = models.PositiveSmallIntegerField(blank=True)
    size = models.CharField(max_length=50, blank=True)
    cover_type = models.CharField(max_length=100, blank=True)
    weight = models.PositiveSmallIntegerField(blank=True)
    age_rest = models.PositiveSmallIntegerField(blank=True)
    photo = models.ImageField(upload_to=save_image_book, blank=True)

    class Meta:
        db_table = 'book'
