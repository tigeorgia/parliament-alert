from django.db import models

# Make sure that contact is active to receive alerts
# and check what kinds of alerts to receive (important?)
class AlertContact(models.Model):
    is_active = models.BooleanField(default=True)
    only_important = models.BooleanField(default=False)

    class Meta:
        abstract = True
