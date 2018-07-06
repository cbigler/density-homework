from django.db import models
from django_extensions.db.models import TimeStampedModel


class Doorway_DPU_Assignment(TimeStampedModel):
    """
    Model to represent the assignment of a DPU to a doorway between two space.

    Keeps track of when the DPU was installed and in which orientation.

    Note: naively assumes DPU never moves, for homework simplicity. Production system should
    support moving a DPU from one doorway to another. One way to accomplish this would be to
    add a `start` and `end` timestamp for each assignment record.
    """
    doorway = models.ForeignKey('density.Doorway', related_name='dpus', null=True, on_delete=models.CASCADE)
    dpu = models.ForeignKey('density.DPU', related_name='doorways', on_delete=models.CASCADE)
    facing_space = models.ForeignKey('density.Space', null=True, db_index=True, on_delete=models.SET_NULL, related_name='facing_spaces')
    behind_space = models.ForeignKey('density.Space', null=True, db_index=True, on_delete=models.SET_NULL, related_name='behind_spaces')







