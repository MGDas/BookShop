from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=250, db_index=True)
    biography = models.TextField(blank=True)
    birthday = models.DateField(blank=True)
    death = models.DateField(blank=True)

    def __str__(self):
        return self.name
