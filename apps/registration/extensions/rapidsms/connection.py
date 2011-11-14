from django.db import models

# Change length of identify field
class ConnectionOAuth(models.Model):
    oauth = models.CharField(max_length=255, default='', blank=True)

    class Meta:
        abstract = True
