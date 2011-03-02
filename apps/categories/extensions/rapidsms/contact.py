from django.db import models
from parliament.apps.categories.models import Category

class ParliamentContact(models.Model):
    categories = models.ManyToManyField(Category,null=True)

    class Meta:
        abstract = True
