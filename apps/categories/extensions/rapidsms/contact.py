from django.db import models
from apps.categories.models import Category

class ParliamentContact(models.Model):
    categories = models.ManyToManyField(Category,null=False)

    class Meta:
        abstract = True
