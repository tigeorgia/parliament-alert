from django.contrib import admin
from apps.alerts.models import ParliamentAlert, AlertSendAttempt

admin.site.register(ParliamentAlert)
admin.site.register(AlertSendAttempt)
