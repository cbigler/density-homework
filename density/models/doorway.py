from django.db import models
from django_extensions.db.models import TimeStampedModel


class Doorway(TimeStampedModel):
    """
    Represent a connection between two spaces.
    """
    name = models.CharField(max_length=200, null=False, blank=False)


