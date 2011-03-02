from django.conf.urls.defaults import *
from . import views

urlpatterns = patterns('',

        url(r'^$',
            views.categories,
            name="categories"),

        url(r'^(?P<pk>\d+)/edit/$',
            views.categories,
            name="category_edit")
        )
