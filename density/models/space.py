from django.db import models
from django_extensions.db.models import TimeStampedModel


class Space(TimeStampedModel):
    """
    Model to represent a tracked space
    """
    name = models.CharField(max_length=200, null=False, blank=False)

