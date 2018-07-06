from django.db import models
from django_extensions.db.models import TimeStampedModel


class DPU(TimeStampedModel):
    """
    Represents a traffic tracking sensor
    """
    name = models.CharField(max_length=200, null=False, blank=False)





