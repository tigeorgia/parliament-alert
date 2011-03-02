from django.conf.urls.defaults import *
from . import views

urlpatterns = patterns('',

    url(r'^$',
        views.alerts,
        name="alerts"),

    url(r'^(?P<pk>\d+)/edit/$',
        views.alerts,
        name="alert_edit"),

    url(r'^(?P<pk>\d+)/send/$',
        views.send,
        name="alert_send")
)
