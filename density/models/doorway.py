from django.db import models
from django_extensions.db.models import TimeStampedModel


class Doorway(TimeStampedModel):
    """
    Model to represent a connection between two spaces. If a Space FK is NULL, it indicates that the
    space is not tracked in the software.
    """
    name = models.CharField(max_length=200, null=False, blank=False)


