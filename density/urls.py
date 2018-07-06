from django.conf.urls import url

from density.api import (
    space_count,
)

urlpatterns = [
    url(r'^space/(?P<space_id>\d+)/count$', space_count.get_space_count, name='space-count'),
]
