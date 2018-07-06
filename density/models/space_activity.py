from django.db import models
from django_extensions.db.models import TimeStampedModel


class Space_Activity(TimeStampedModel):
    """
    Model to represent activity reported by a DPU
    """
    space = models.ForeignKey('density.Space', null=True, on_delete=models.CASCADE)
    count = models.IntegerField()
    activity_ts = models.DateTimeField()

    class Meta:
        index_together = ('space', 'activity_ts')





