from django.db import models

# Create your models here.

# Basically a system of tags for messages about Parliament
# We plan to use this for committees, topics, etc.
class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50)
