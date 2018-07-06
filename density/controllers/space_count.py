from django.db.models import Sum

from density.models import Space_Activity


def get_space_count(space, at_ts=None):
    """
    Returns the Space's occupancy count at the point in time specified

    :param space: the :class:`Space` to get the count for
    :param at_ts: timestamp or None for current

    :return: the occupancy count for the space at the point in time specified
    """

    if not space:
        raise ValueError('Space is required to get space count')

    q = Space_Activity.objects.filter(space=space)
    if at_ts:
        q = q.filter(activity_ts__lte=at_ts)

    return q.aggregate(Sum('count'))['count__sum'] or 0


