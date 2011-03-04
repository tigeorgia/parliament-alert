from django.db import models
# Create your models here.

# Basically a system of tags for messages about Parliament
# We plan to use this for committees, topics, etc.
class Category(models.Model):
    name = models.CharField(max_length=200)
#    slug = models.SlugField(max_length=50)
    #Comma-delimited keywords that will match this Category for subscription
    keywords = models.TextField(max_length=500,blank=True)

    def __unicode__(self):
        return self.name
